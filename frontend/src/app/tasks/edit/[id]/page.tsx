'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Header from '@/components/Header';
import TaskForm from '@/components/TaskForm';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useAuth } from '@/contexts/AuthContext';

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

export default function EditTaskPage() {
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

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${currentUserId}/tasks/${id}?token=${token}`
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to fetch task: ${response.status} ${errorText}`);
      }

      const data = await response.json();
      setTask(data.task || data);
    } catch (error) {
      console.error('Error fetching task:', error);
    } finally {
      setLoading(false);
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
              <p className="text-gray-600">The task you are trying to edit does not exist or has been deleted.</p>
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
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800">Edit Task</h1>
            <p className="text-gray-600 mt-2">Update the task details below and save changes.</p>
          </div>
          <div className="bg-white shadow-md rounded-xl p-6">
            <TaskForm task={task} isEdit={true} />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
