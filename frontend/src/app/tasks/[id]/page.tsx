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
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <Header />
        <div className="container mx-auto px-4 py-16">
          <div className="mb-10 text-center">
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Task Details
            </h1>
            <p className="text-gray-600 mt-2 text-lg">
              View and manage your task information
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-10 border border-gray-200/50 transform hover:scale-[1.01] transition-transform duration-300">
              <div className="flex flex-col lg:flex-row justify-between items-start gap-6 mb-8">
                <div className="flex-1">
                  <h2 className={`text-3xl font-bold mb-4 ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                    {task.title}
                  </h2>

                  {task.description && (
                    <div className="mb-6">
                      <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                        </svg>
                        Description
                      </h3>
                      <div className="bg-gray-50 p-4 rounded-xl border border-gray-100">
                        <p className="text-gray-700 leading-relaxed">{task.description}</p>
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex flex-col items-end gap-4">
                  <span className={`px-4 py-2 rounded-2xl text-sm font-bold shadow-lg ${
                    task.priority === 'high' ? 'bg-gradient-to-r from-red-100 to-red-200 text-red-800' :
                    task.priority === 'medium' ? 'bg-gradient-to-r from-yellow-100 to-yellow-200 text-yellow-800' :
                    'bg-gradient-to-r from-green-100 to-green-200 text-green-800'
                  }`}>
                    {task.priority.toUpperCase()} PRIORITY
                  </span>

                  <div className={`px-4 py-2 rounded-2xl text-sm font-bold shadow-lg ${
                    task.completed ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800' : 'bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-800'
                  }`}>
                    {task.completed ? '✓ COMPLETED' : '⏳ PENDING'}
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-2xl border border-blue-100/50">
                  <h3 className="text-sm font-semibold text-blue-700 mb-3 flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Status Information
                  </h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Current Status:</span>
                      <span className={`font-semibold ${task.completed ? 'text-green-600' : 'text-yellow-600'}`}>
                        {task.completed ? 'Completed' : 'Pending'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Priority Level:</span>
                      <span className={`font-semibold ${
                        task.priority === 'high' ? 'text-red-600' :
                        task.priority === 'medium' ? 'text-yellow-600' :
                        'text-green-600'
                      }`}>
                        {task.priority.toUpperCase()}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-2xl border border-purple-100/50">
                  <h3 className="text-sm font-semibold text-purple-700 mb-3 flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Timeline
                  </h3>
                  <div className="space-y-2">
                    {task.due_date && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Due Date:</span>
                        <span className="font-semibold text-purple-600">
                          {new Date(task.due_date).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric'
                          })}
                        </span>
                      </div>
                    )}
                    <div className="flex justify-between">
                      <span className="text-gray-600">Created:</span>
                      <span className="font-semibold text-purple-600">
                        {new Date(task.created_at).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric'
                        })}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Last Updated:</span>
                      <span className="font-semibold text-purple-600">
                        {new Date(task.updated_at).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric'
                        })}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap justify-center gap-4">
                <a href={`/tasks/edit/${task.id}`} className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold py-3 px-8 rounded-2xl shadow-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl group relative overflow-hidden flex items-center gap-2">
                  <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                  <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
                    <svg className="w-5 h-5 group-hover:rotate-12 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Edit Task
                  </span>
                </a>

                <button onClick={toggleTaskCompletion} className={`bg-gradient-to-r ${
                  task.completed ? 'from-yellow-500 to-amber-600 hover:from-yellow-600 hover:to-amber-700' : 'from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700'
                } text-white font-bold py-3 px-8 rounded-2xl shadow-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl group relative overflow-hidden flex items-center gap-2`}>
                  <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                  <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
                    <svg className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {task.completed ? 'Mark Incomplete' : 'Mark Complete'}
                  </span>
                </button>

                <button onClick={deleteTask} className="bg-gradient-to-r from-red-500 to-rose-600 hover:from-red-600 hover:to-rose-700 text-white font-bold py-3 px-8 rounded-2xl shadow-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl group relative overflow-hidden flex items-center gap-2">
                  <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                  <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
                    <svg className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Delete Task
                  </span>
                </button>
              </div>

              <div className="flex flex-wrap justify-center gap-4 mt-6">
                <a href="/tasks" className="bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white font-medium py-2.5 px-6 rounded-xl shadow-md transition-all duration-300 transform hover:scale-105 group relative overflow-hidden flex items-center gap-2">
                  <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                  <span className="relative flex items-center gap-1 group-hover:gap-2 transition-all duration-300">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    All Tasks
                  </span>
                </a>

                <a href="/dashboard" className="bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white font-medium py-2.5 px-6 rounded-xl shadow-md transition-all duration-300 transform hover:scale-105 group relative overflow-hidden flex items-center gap-2">
                  <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                  <span className="relative flex items-center gap-1 group-hover:gap-2 transition-all duration-300">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z" />
                    </svg>
                    Dashboard
                  </span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
