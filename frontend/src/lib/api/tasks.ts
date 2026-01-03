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

interface CreateTaskData {
  title: string;
  description?: string;
  priority?: string;
  due_date?: string;
}

interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: string;
  due_date?: string;
}

interface FilterParams {
  completed?: string;
  priority?: string;
  sort?: string;
  order?: string;
}

export const tasksAPI = {
  async getTasks(userId: string, token: string, filters?: FilterParams): Promise<Task[]> {
    console.log('Attempting to get tasks:', { userId, hasToken: !!token, filters });

    // Decode the token to get the user ID from the 'sub' field to ensure consistency
    let actualUserId = userId;
    if (!userId || userId === 'undefined') {
      const tokenParts = token.split('.');
      if (tokenParts.length === 3) {
        const payload = JSON.parse(atob(tokenParts[1]));
        actualUserId = payload.sub;
      }
    }

    if (!actualUserId || actualUserId === 'undefined') {
      throw new Error('User ID not found in token');
    }

    console.log('Final user ID for get tasks request:', actualUserId);

    let url = `${process.env.NEXT_PUBLIC_API_URL}/api/${actualUserId}/tasks?token=${token}`;

    if (filters) {
      const params = new URLSearchParams();
      if (filters.completed !== undefined) params.append('completed', filters.completed);
      if (filters.priority !== undefined) params.append('priority', filters.priority);
      if (filters.sort !== undefined) params.append('sort', filters.sort);
      if (filters.order !== undefined) params.append('order', filters.order);
      url += `&${params.toString()}`;
    }

    console.log('Get tasks request URL:', url);

    // Set a timeout for the fetch request
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

    try {
      const response = await fetch(url, {
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Get tasks error:', response.status, errorText);
        throw new Error(`Failed to fetch tasks: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      return data.tasks || data; // Handle both formats
    } catch (fetchError: any) {
      clearTimeout(timeoutId);

      if (fetchError.name === 'AbortError') {
        console.error('Get tasks request timed out:', url);
        throw new Error('Request timed out. Please try again.');
      } else {
        console.error('Network error during get tasks request:', fetchError, url);
        throw new Error('Network error. Please check your connection and try again.');
      }
    }
  },

  async getTask(userId: string, taskId: string, token: string): Promise<Task> {
    console.log('Attempting to get task:', { userId, taskId, hasToken: !!token });

    // Decode the token to get the user ID from the 'sub' field to ensure consistency
    let actualUserId = userId;
    if (!userId || userId === 'undefined') {
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          actualUserId = payload.sub;
          console.log('Extracted user ID from token for getTask:', actualUserId);
        } else {
          console.error('Invalid token format for getTask');
          throw new Error('Invalid token format');
        }
      } catch (decodeError) {
        console.error('Error decoding token for getTask:', decodeError);
        throw new Error('Failed to decode token to get user ID');
      }
    }

    if (!actualUserId || actualUserId === 'undefined') {
      throw new Error('User ID not found in token');
    }

    console.log('Final user ID for get task request:', actualUserId);

    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/${actualUserId}/tasks/${taskId}?token=${token}`;
    console.log('Get task request URL:', url);

    // Set a timeout for the fetch request
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

    try {
      const response = await fetch(url, {
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Get task error:', response.status, errorText);
        throw new Error(`Failed to fetch task: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      return data.task || data; // Handle both formats
    } catch (fetchError: any) {
      clearTimeout(timeoutId);

      if (fetchError.name === 'AbortError') {
        console.error('Get task request timed out:', url);
        throw new Error('Request timed out. Please try again.');
      } else {
        console.error('Network error during get task request:', fetchError, url);
        throw new Error('Network error. Please check your connection and try again.');
      }
    }
  },

  async createTask(userId: string, token: string, taskData: CreateTaskData): Promise<Task> {
    console.log('Attempting to create task:', { userId, hasToken: !!token, taskData });

    // Decode the token to get the user ID from the 'sub' field to ensure consistency
    let actualUserId = userId;
    if (!userId || userId === 'undefined') {
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          actualUserId = payload.sub;
          console.log('Extracted user ID from token for createTask:', actualUserId);
        } else {
          console.error('Invalid token format for createTask');
          throw new Error('Invalid token format');
        }
      } catch (decodeError) {
        console.error('Error decoding token for createTask:', decodeError);
        throw new Error('Failed to decode token to get user ID');
      }
    }

    if (!actualUserId || actualUserId === 'undefined') {
      throw new Error('User ID not found in token');
    }

    console.log('Final user ID for create task request:', actualUserId);

    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/${actualUserId}/tasks?token=${token}`;
    console.log('Create task request URL:', url);

    // Set a timeout for the fetch request
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Create task error:', response.status, errorText);
        throw new Error(`Failed to create task: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      return data.task || data; // Handle both formats
    } catch (fetchError: any) {
      clearTimeout(timeoutId);

      if (fetchError.name === 'AbortError') {
        console.error('Create task request timed out:', url);
        throw new Error('Request timed out. Please try again.');
      } else {
        console.error('Network error during create task request:', fetchError, url);
        throw new Error('Network error. Please check your connection and try again.');
      }
    }
  },

  async updateTask(userId: string, taskId: string, token: string, taskData: UpdateTaskData): Promise<Task> {
    console.log('Attempting to update task:', { userId, taskId, hasToken: !!token, taskData });

    // Decode the token to get the user ID from the 'sub' field to ensure consistency
    let actualUserId = userId;
    if (!userId || userId === 'undefined') {
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          actualUserId = payload.sub;
          console.log('Extracted user ID from token for updateTask:', actualUserId);
        } else {
          console.error('Invalid token format for updateTask');
          throw new Error('Invalid token format');
        }
      } catch (decodeError) {
        console.error('Error decoding token for updateTask:', decodeError);
        throw new Error('Failed to decode token to get user ID');
      }
    }

    if (!actualUserId || actualUserId === 'undefined') {
      throw new Error('User ID not found in token');
    }

    console.log('Final user ID for update task request:', actualUserId);

    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/${actualUserId}/tasks/${taskId}?token=${encodeURIComponent(token)}`;
    console.log('Update task request URL:', url);

    // Set a timeout for the fetch request
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

    try {
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Update task error:', response.status, errorText);
        throw new Error(`Failed to update task: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      return data.task || data; // Handle both formats
    } catch (fetchError: any) {
      clearTimeout(timeoutId);

      if (fetchError.name === 'AbortError') {
        console.error('Update task request timed out:', url);
        throw new Error('Request timed out. Please try again.');
      } else {
        console.error('Network error during update task request:', fetchError, url);
        throw new Error('Network error. Please check your connection and try again.');
      }
    }
  },


  async toggleTaskCompletion(userId: string, taskId: string, token: string, completed: boolean): Promise<Task> {
    console.log('Attempting to toggle task completion:', { userId, taskId, completed, hasToken: !!token });

    // Decode the token to get the user ID from the 'sub' field to ensure consistency
    let actualUserId = userId;
    if (!userId || userId === 'undefined') {
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          actualUserId = payload.sub;
          console.log('Extracted user ID from token for toggle:', actualUserId);
        } else {
          console.error('Invalid token format for toggle');
          throw new Error('Invalid token format');
        }
      } catch (decodeError) {
        console.error('Error decoding token for toggle:', decodeError);
        throw new Error('Failed to decode token to get user ID');
      }
    }

    if (!actualUserId || actualUserId === 'undefined') {
      throw new Error('User ID not found in token');
    }

    console.log('Final user ID for toggle request:', actualUserId);

    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/${actualUserId}/tasks/${taskId}/complete?completed=${completed}&token=${encodeURIComponent(token)}`;
    console.log('Toggle completion request URL:', url);

    // Set a timeout for the fetch request
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

    try {
      const response = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Toggle completion error:', response.status, errorText);
        throw new Error(`Failed to update task completion: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      return data.task || data; // Handle both formats
    } catch (fetchError: any) {
      clearTimeout(timeoutId);

      if (fetchError.name === 'AbortError') {
        console.error('Toggle completion request timed out:', url);
        throw new Error('Request timed out. Please try again.');
      } else {
        console.error('Network error during toggle completion request:', fetchError, url);
        throw new Error('Network error. Please check your connection and try again.');
      }
    }
  },

  async deleteTask(userId: string, taskId: string, token: string): Promise<void> {
    console.log('Attempting to delete task:', { userId, taskId, hasToken: !!token });

    // Decode the token to get the user ID from the 'sub' field to ensure consistency
    let actualUserId = userId;
    if (!userId || userId === 'undefined') {
      try {
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          actualUserId = payload.sub;
          console.log('Extracted user ID from token for deleteTask:', actualUserId);
        } else {
          console.error('Invalid token format for deleteTask');
          throw new Error('Invalid token format');
        }
      } catch (decodeError) {
        console.error('Error decoding token for deleteTask:', decodeError);
        throw new Error('Failed to decode token to get user ID');
      }
    }

    if (!actualUserId || actualUserId === 'undefined') {
      throw new Error('User ID not found in token');
    }

    console.log('Final user ID for delete task request:', actualUserId);

    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/${actualUserId}/tasks/${taskId}?token=${encodeURIComponent(token)}`;
    console.log('Delete task request URL:', url);

    // Set a timeout for the fetch request
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

    try {
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Delete task error:', response.status, errorText);
        throw new Error(`Failed to delete task: ${response.status} - ${errorText}`);
      }

      console.log('Task deleted successfully');
      return; // DELETE requests typically don't return a body
    } catch (fetchError: any) {
      clearTimeout(timeoutId);

      if (fetchError.name === 'AbortError') {
        console.error('Delete task request timed out:', url);
        throw new Error('Request timed out. Please try again.');
      } else {
        console.error('Network error during delete task request:', fetchError, url);
        throw new Error('Network error. Please check your connection and try again.');
      }
    }
  },
};