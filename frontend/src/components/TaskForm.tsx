'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { tasksAPI } from '@/lib/api/tasks';

interface TaskFormProps {
  task?: {
    id: string;
    title: string;
    description: string | null;
    priority: string;
    due_date: string | null;
  };
  isEdit?: boolean;
}

interface TaskData {
  title: string;
  description: string;
  priority: string;
  due_date: string;
}

export default function TaskForm({ task, isEdit = false }: TaskFormProps) {
  const { state } = useAuth();
  const router = useRouter();

  const [formData, setFormData] = useState<TaskData>({
    title: task?.title || '',
    description: task?.description || '',
    priority: task?.priority || 'medium',
    due_date: task?.due_date || '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    // Check if user is authenticated
    if (!state.token || !state.user?.id) {
      console.error('User not authenticated');
      router.push('/login');
      return;
    }

    setLoading(true);

    try {
      const token = localStorage.getItem('auth_token');
      if (!token || !state.user?.id || state.user.id === 'undefined') {
        console.error('User not authenticated');
        router.push('/login');
        return;
      }

      if (isEdit && task) {
        // Update existing task using tasksAPI
        await tasksAPI.updateTask(state.user.id, task.id, token, {
          title: formData.title,
          description: formData.description,
          priority: formData.priority,
          due_date: formData.due_date ? new Date(formData.due_date).toISOString() : undefined,
        });
      } else {
        // Create new task using tasksAPI
        await tasksAPI.createTask(state.user.id, token, {
          title: formData.title,
          description: formData.description,
          priority: formData.priority,
          due_date: formData.due_date ? new Date(formData.due_date).toISOString() : undefined,
        });
      }

      router.push('/tasks');
    } catch (error: any) {
      console.error('Error submitting task:', error);
      alert('Error submitting task: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Show loading state if user data is not yet available
  if (!state.token || !state.user?.id || state.user.id === 'undefined') {
    return (
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
        <p className="text-center mt-4">Loading...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow rounded-lg p-6">
      <div className="mb-4">
        <label htmlFor="title" className="block text-gray-700 font-medium mb-2">
          Title *
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.title ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Task title"
        />
        {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
      </div>

      <div className="mb-4">
        <label htmlFor="description" className="block text-gray-700 font-medium mb-2">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Task description"
        ></textarea>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="priority" className="block text-gray-700 font-medium mb-2">
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div>
          <label htmlFor="due_date" className="block text-gray-700 font-medium mb-2">
            Due Date
          </label>
          <input
            type="date"
            id="due_date"
            name="due_date"
            value={formData.due_date}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="flex justify-end space-x-4">
        <a
          href="/tasks"
          className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
        >
          Cancel
        </a>
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
        >
          {loading ? (isEdit ? 'Updating...' : 'Creating...') : isEdit ? 'Update Task' : 'Create Task'}
        </button>
      </div>
    </form>
  );
}