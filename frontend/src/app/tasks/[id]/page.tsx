'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Header from '@/components/Header';
import { tasksAPI } from '@/lib/api/tasks';

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

export default function TaskDetailPage() {
  const { id } = useParams();
  const { state } = useAuth();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTask();
  }, [id]);

  const fetchTask = async () => {
    try {
      let attempts = 0;
      let currentToken = state.token;
      let currentUserId = state.user?.id;

      while (!currentToken && !currentUserId && attempts < 10) {
        await new Promise(resolve => setTimeout(resolve, 100));
        currentToken = state.token;
        currentUserId = state.user?.id;
        attempts++;
      }

      if (!currentToken || !currentUserId) {
        const tokenFromStorage = localStorage.getItem('auth_token');
        if (!tokenFromStorage) throw new Error('User not authenticated');

        try {
          const tokenParts = tokenFromStorage.split('.');
          if (tokenParts.length === 3) {
            const payload = JSON.parse(atob(tokenParts[1]));
            currentUserId = payload.sub;
          }
        } catch {
          throw new Error('User not authenticated');
        }
      }

      const token = localStorage.getItem('auth_token');
      if (!token) throw new Error('No authentication token found');

      if (!currentUserId || currentUserId === 'undefined') throw new Error('User ID is not valid');

      const taskData = await tasksAPI.getTask(currentUserId, id as string, token);
      setTask(taskData);
    } catch (error: any) {
      console.error('Error fetching task:', error);
      alert('Error fetching task: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async () => {
    if (!task) return;
    try {
      const token = localStorage.getItem('auth_token');
      if (!token || !state.user?.id || state.user.id === 'undefined') throw new Error('User not authenticated');

      const updatedTask = await tasksAPI.toggleTaskCompletion(state.user.id, task.id, token, !task.completed);
      setTask(updatedTask);

      window.dispatchEvent(new CustomEvent('taskUpdated'));
      localStorage.setItem('taskUpdated', Date.now().toString());
    } catch (error) {
      console.error('Error updating task completion:', error);
      alert('Error updating task: ' + (error as Error).message);
    }
  };

  const deleteTask = async () => {
    if (!task) return;
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token || !state.user?.id || state.user.id === 'undefined') throw new Error('User not authenticated');

        await tasksAPI.deleteTask(state.user.id, task.id, token);

        window.dispatchEvent(new CustomEvent('taskDeleted'));
        localStorage.setItem('taskDeleted', Date.now().toString());

        window.location.href = '/tasks';
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Error deleting task: ' + (error as Error).message);
      }
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gray-100">
          <Header />
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <p className="text-gray-700 text-lg font-medium">Loading task...</p>
            </div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  if (!task) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gray-100">
          <Header />
          <div className="flex items-center justify-center h-64">
            <div className="bg-white shadow-md rounded-xl p-6 text-center">
              <h1 className="text-2xl font-bold text-gray-800 mb-2">Task not found</h1>
              <p className="text-gray-600">This task might have been deleted or does not exist.</p>
            </div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <Header />
        <div className="container mx-auto px-4 py-8">
          <div className="mb-8 flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-800">Task Details</h1>
          </div>

          <div className="bg-white shadow-md rounded-xl p-6">
            <div className="flex items-start justify-between">
              <h2 className={`text-2xl font-bold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {task.title}
              </h2>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                task.priority === 'high' ? 'bg-red-100 text-red-800' :
                task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {task.priority}
              </span>
            </div>

            {task.description && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold text-gray-700">Description</h3>
                <p className="text-gray-600 mt-1">{task.description}</p>
              </div>
            )}

            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h3 className="text-sm font-medium text-gray-500">Status</h3>
                <p className={`mt-1 ${task.completed ? 'text-green-600' : 'text-yellow-600'}`}>
                  {task.completed ? 'Completed' : 'Pending'}
                </p>
              </div>

              {task.due_date && (
                <div>
                  <h3 className="text-sm font-medium text-gray-500">Due Date</h3>
                  <p className="mt-1 text-gray-900">
                    {new Date(task.due_date).toLocaleDateString()}
                  </p>
                </div>
              )}

              <div>
                <h3 className="text-sm font-medium text-gray-500">Created</h3>
                <p className="mt-1 text-gray-900">{new Date(task.created_at).toLocaleString()}</p>
              </div>

              <div>
                <h3 className="text-sm font-medium text-gray-500">Last Updated</h3>
                <p className="mt-1 text-gray-900">{new Date(task.updated_at).toLocaleString()}</p>
              </div>
            </div>

            <div className="mt-8 flex flex-wrap gap-4">
              <a href={`/tasks/edit/${task.id}`} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Edit Task
              </a>
              <button onClick={toggleTaskCompletion} className={`${task.completed ? 'bg-yellow-500 hover:bg-yellow-700' : 'bg-green-500 hover:bg-green-700'} text-white font-bold py-2 px-4 rounded`}>
                {task.completed ? 'Mark Incomplete' : 'Mark Complete'}
              </button>
              <button onClick={deleteTask} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                Delete Task
              </button>
              <a href="/tasks" className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
                Back to Tasks
              </a>
              <a href="/dashboard" className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">
                Back to Dashboard
              </a>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
