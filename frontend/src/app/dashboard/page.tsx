'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Header from '@/components/Header';

interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: string;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const { state, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, [state.user?.id]);

  useEffect(() => {
    const handleTaskDeleted = () => fetchTasks();
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'taskDeleted') fetchTasks();
    };
    window.addEventListener('taskDeleted', handleTaskDeleted);
    window.addEventListener('storage', handleStorageChange);
    return () => {
      window.removeEventListener('taskDeleted', handleTaskDeleted);
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${state.user?.id}/tasks?token=${token}`
      );
      if (response.ok) {
        const data = await response.json();
        setTasks(data.slice(0, 5));
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityClass = (priority: string) => {
    if (priority === 'high') return 'bg-red-200 text-red-800';
    if (priority === 'medium') return 'bg-yellow-200 text-yellow-800';
    return 'bg-green-200 text-green-800';
  };

  const getStatusClass = (completed: boolean) =>
    completed
      ? 'bg-green-200 text-green-800'
      : 'bg-gray-200 text-gray-800';

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <Header />

        <div className="container mx-auto px-4 py-6">
          {/* Welcome Card */}
          <div className="bg-white shadow rounded-xl p-6 mb-6">
            <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4">
              <h1 className="text-2xl md:text-3xl font-bold">Dashboard</h1>

              <button
                onClick={logout}
                className="w-full md:w-auto bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-xl"
              >
                Logout
              </button>
            </div>

            <h2 className="text-lg md:text-xl mt-3 font-semibold">
              Welcome, {state.user?.name}!
            </h2>
            <p className="text-sm md:text-base text-gray-600">
              Email: {state.user?.email}
            </p>
          </div>

          {/* Tasks Section */}
          <div className="bg-white shadow rounded-xl p-6">
            <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-4 mb-4">
              <h2 className="text-xl md:text-2xl font-bold">Your Tasks</h2>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row flex-wrap gap-2">
                <button
                  onClick={fetchTasks}
                  className="bg-gray-500 hover:bg-gray-600 text-white py-2 px-4 rounded-xl"
                >
                  Refresh
                </button>

                <a
                  href="/tasks/new"
                  className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-xl text-center"
                >
                  Create Task
                </a>

                <a
                  href="/tasks"
                  className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-xl text-center"
                >
                  View Tasks
                </a>
              </div>
            </div>

            {/* Loading */}
            {loading && (
              <div className="flex justify-center py-10">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"></div>
              </div>
            )}

            {/* No Tasks */}
            {!loading && tasks.length === 0 && (
              <p className="text-center text-gray-600 py-6">
                No tasks found.{' '}
                <a href="/tasks/new" className="text-blue-500 underline">
                  Create your first task
                </a>
              </p>
            )}

            {/* MOBILE VIEW – CARD */}
            <div className="md:hidden space-y-4">
              {tasks.map((task) => (
                <div key={task.id} className="border rounded-xl p-4">
                  <h3 className="font-semibold">{task.title}</h3>

                  {task.description && (
                    <p className="text-sm text-gray-500">
                      {task.description}
                    </p>
                  )}

                  <div className="flex flex-wrap gap-2 mt-3">
                    <span className={`px-2 py-1 text-xs rounded-full ${getPriorityClass(task.priority)}`}>
                      {task.priority}
                    </span>

                    <span className={`px-2 py-1 text-xs rounded-full ${getStatusClass(task.completed)}`}>
                      {task.completed ? 'Completed' : 'Pending'}
                    </span>
                  </div>

                  <p className="text-xs text-gray-500 mt-2">
                    Due: {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'No date'}
                  </p>
                </div>
              ))}
            </div>

            {/* DESKTOP VIEW – TABLE */}
            <div className="hidden md:block overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-sm">Title</th>
                    <th className="px-4 py-2 text-left text-sm">Priority</th>
                    <th className="px-4 py-2 text-left text-sm">Status</th>
                    <th className="px-4 py-2 text-left text-sm">Due Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {tasks.map((task) => (
                    <tr key={task.id} className="hover:bg-gray-50">
                      <td className="px-4 py-2">{task.title}</td>
                      <td className="px-4 py-2">
                        <span className={`px-2 py-1 text-xs rounded-full ${getPriorityClass(task.priority)}`}>
                          {task.priority}
                        </span>
                      </td>
                      <td className="px-4 py-2">
                        <span className={`px-2 py-1 text-xs rounded-full ${getStatusClass(task.completed)}`}>
                          {task.completed ? 'Completed' : 'Pending'}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-sm">
                        {task.due_date
                          ? new Date(task.due_date).toLocaleDateString()
                          : 'No due date'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
