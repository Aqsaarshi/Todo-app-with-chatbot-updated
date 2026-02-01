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
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <Header />
        <div className="container mx-auto px-4 py-16">
          <div className="mb-10 text-center">
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
              Edit Task
            </h1>
            <p className="text-gray-600 text-lg">
              Update your task details and save changes
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-10 border border-gray-200/50 transform hover:scale-[1.01] transition-transform duration-300">
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                  {task.title}
                </h2>
                <p className="text-gray-600">
                  {task.description || 'No description provided'}
                </p>

                <div className="flex flex-wrap gap-4 mt-4">
                  <span className={`px-4 py-2 rounded-2xl text-sm font-bold shadow-lg ${
                    task.priority === 'high' ? 'bg-gradient-to-r from-red-100 to-red-200 text-red-800' :
                    task.priority === 'medium' ? 'bg-gradient-to-r from-yellow-100 to-yellow-200 text-yellow-800' :
                    'bg-gradient-to-r from-green-100 to-green-200 text-green-800'
                  }`}>
                    {task.priority.toUpperCase()} PRIORITY
                  </span>

                  <span className={`px-4 py-2 rounded-2xl text-sm font-bold shadow-lg ${
                    task.completed ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800' : 'bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-800'
                  }`}>
                    {task.completed ? '✓ COMPLETED' : '⏳ PENDING'}
                  </span>

                  {task.due_date && (
                    <span className="px-4 py-2 rounded-2xl text-sm font-bold shadow-lg bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-800">
                      <svg className="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      Due: {new Date(task.due_date).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    </span>
                  )}
                </div>
              </div>

              <div className="border-t border-gray-200/50 pt-8">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center gap-3">
                  <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Update Task Details
                </h3>
                <TaskForm task={task} isEdit={true} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
