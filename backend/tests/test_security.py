import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from uuid import uuid4
from backend.src.main import app
from backend.src.database import get_session
from backend.src.models.user import User
from backend.src.models.task import Task
from backend.src.auth.jwt import get_password_hash


# Set up a test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_user_data_isolation(session: Session, client: TestClient):
    """Test that users can only access their own data"""

    # Create two users
    user1 = User(
        email="user1@example.com",
        name="User One",
        password_hash=get_password_hash("password123")
    )
    session.add(user1)
    session.commit()
    session.refresh(user1)

    user2 = User(
        email="user2@example.com",
        name="User Two",
        password_hash=get_password_hash("password123")
    )
    session.add(user2)
    session.commit()
    session.refresh(user2)

    # Create tasks for user1
    task1 = Task(
        title="User 1 Task",
        user_id=user1.id,
        completed=False,
        priority="medium"
    )
    session.add(task1)
    session.commit()
    session.refresh(task1)

    # Create tasks for user2
    task2 = Task(
        title="User 2 Task",
        user_id=user2.id,
        completed=False,
        priority="medium"
    )
    session.add(task2)
    session.commit()
    session.refresh(task2)

    # Authenticate user1 and get token
    response = client.post("/api/auth/login", data={
        "email": "user1@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    token1 = response.json()["token"]

    # Authenticate user2 and get token
    response = client.post("/api/auth/login", data={
        "email": "user2@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    token2 = response.json()["token"]

    # User1 should be able to access their own tasks
    response = client.get(f"/api/{user1.id}/tasks", params={"token": token1})
    assert response.status_code == 200
    user1_tasks = response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["id"] == str(task1.id)

    # User2 should be able to access their own tasks
    response = client.get(f"/api/{user2.id}/tasks", params={"token": token2})
    assert response.status_code == 200
    user2_tasks = response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["id"] == str(task2.id)

    # User1 should NOT be able to access user2's tasks
    response = client.get(f"/api/{user2.id}/tasks", params={"token": token1})
    assert response.status_code == 403  # Forbidden

    # User2 should NOT be able to access user1's tasks
    response = client.get(f"/api/{user1.id}/tasks", params={"token": token2})
    assert response.status_code == 403  # Forbidden

    # User1 should NOT be able to access a specific task that belongs to user2
    response = client.get(f"/api/{user2.id}/tasks/{task2.id}", params={"token": token1})
    assert response.status_code == 403  # Forbidden


def test_cross_user_task_access_prevention(session: Session, client: TestClient):
    """Test that users cannot access tasks belonging to other users"""

    # Create two users
    user1 = User(
        email="user1@example.com",
        name="User One",
        password_hash=get_password_hash("password123")
    )
    session.add(user1)
    session.commit()
    session.refresh(user1)

    user2 = User(
        email="user2@example.com",
        name="User Two",
        password_hash=get_password_hash("password123")
    )
    session.add(user2)
    session.commit()
    session.refresh(user2)

    # Create a task for user2
    task2 = Task(
        title="User 2 Task",
        user_id=user2.id,
        completed=False,
        priority="medium"
    )
    session.add(task2)
    session.commit()
    session.refresh(task2)

    # Authenticate user1
    response = client.post("/api/auth/login", data={
        "email": "user1@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    token1 = response.json()["token"]

    # User1 should NOT be able to access user2's task even if they know the task ID
    response = client.get(f"/api/{user2.id}/tasks/{task2.id}", params={"token": token1})
    assert response.status_code == 403  # Forbidden

    # User1 should NOT be able to update user2's task
    response = client.put(f"/api/{user2.id}/tasks/{task2.id}",
                         params={"token": token1},
                         json={"title": "Hacked task"})
    assert response.status_code == 403  # Forbidden

    # User1 should NOT be able to delete user2's task
    response = client.delete(f"/api/{user2.id}/tasks/{task2.id}", params={"token": token1})
    assert response.status_code == 403  # Forbidden