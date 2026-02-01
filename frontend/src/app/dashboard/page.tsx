'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Header from '@/components/Header';
import NewChatBotIcon from '@/components/NewChatBotIcon';
import NewChatInterface from '@/components/NewChatInterface';
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

export default function DashboardPage() {
  const { state, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  useEffect(() => {
    if (state.user?.id) {
      fetchTasks();
    }
  }, [state.user?.id]);

  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'taskDeleted' && state.user?.id) {
        fetchTasks();
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [state.user?.id]);

  const fetchTasks = async () => {
    if (!state.user?.id) {
      console.error('User not authenticated');
      return;
    }

    try {
      setLoading(true);
      const token = localStorage.getItem('auth_token');

      if (!token) {
        throw new Error('Authentication token not found');
      }

      // Use the tasksAPI to fetch tasks
      const allTasks = await tasksAPI.getTasks(state.user.id, token);
      // Only show first 5 tasks on dashboard
      setTasks(allTasks.slice(0, 5));
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
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
        <Header />

        <div className="container mx-auto px-4 py-8">
          {/* Welcome Card with enhanced styling */}
          <div className="card p-8 mb-8 animate-fade-in">
            <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-6">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Dashboard
                </h1>
                <h2 className="text-xl md:text-2xl mt-3 font-semibold text-gray-800">
                  Welcome, {state.user?.name}!
                </h2>
                <p className="text-gray-600 mt-2">
                  Email: {state.user?.email}
                </p>
              </div>

              <button
                onClick={logout}
                className="bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 group relative overflow-hidden w-full md:w-auto"
              >
                <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                <span className="relative flex items-center justify-center gap-2 group-hover:gap-3 transition-all duration-300">
                  <svg className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Logout
                </span>
              </button>
            </div>
          </div>

          {/* Tasks Section with enhanced styling */}
          <div className="card p-8">
            <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-6 mb-8">
              <h2 className="text-2xl md:text-3xl font-bold text-gray-800">
                Your Tasks
              </h2>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row flex-wrap gap-4">
                <button
                  onClick={fetchTasks}
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 group relative overflow-hidden flex items-center justify-center gap-2"
                >
                  <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                  <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
                    <svg className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Refresh
                  </span>
                </button>

                <a
                  href="/tasks/new"
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 group relative overflow-hidden flex items-center justify-center gap-2"
                >
                  <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                  <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
                    <svg className="w-4 h-4 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Create Task
                  </span>
                </a>

                <a
                  href="/tasks"
                  className="bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 group relative overflow-hidden flex items-center justify-center gap-2"
                >
                  <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                  <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
                    <svg className="w-4 h-4 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    View Tasks
                  </span>
                </a>
              </div>
            </div>

            {/* Loading */}
            {loading && (
              <div className="flex justify-center py-16">
                <div className="spinner"></div>
              </div>
            )}

            {/* No Tasks */}
            {!loading && tasks.length === 0 && (
              <div className="text-center py-12">
                <div className="mx-auto w-24 h-24 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-6">
                  <svg className="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <p className="text-gray-600 text-lg mb-6">
                  No tasks found.
                </p>
                <a href="/tasks/new" className="btn-primary inline-flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Create your first task
                </a>
              </div>
            )}

            {/* MOBILE VIEW – CARD */}
            <div className="md:hidden space-y-6">
              {tasks.map((task, index) => (
                <div
                  key={task.id}
                  className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-300 animate-fade-in"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-semibold text-lg text-gray-800">{task.title}</h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getPriorityClass(task.priority)}`}>
                      {task.priority}
                    </span>
                  </div>

                  {task.description && (
                    <p className="text-gray-600 mb-4 leading-relaxed">
                      {task.description}
                    </p>
                  )}

                  <div className="flex flex-wrap gap-3 items-center">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusClass(task.completed)}`}>
                      {task.completed ? 'Completed' : 'Pending'}
                    </span>

                    <div className="text-sm text-gray-500 flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      {task.due_date
                        ? new Date(task.due_date).toLocaleDateString()
                        : 'No due date'}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* DESKTOP VIEW – TABLE */}
            <div className="hidden md:block overflow-x-auto rounded-2xl shadow-xl">
              <table className="min-w-full divide-y divide-gray-200 border border-gray-200/60 rounded-2xl overflow-hidden">
                <thead className="bg-gradient-to-r from-indigo-100/80 to-purple-100/80 border-b-2 border-gray-200/70">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-800 uppercase tracking-wide border-r border-gray-200/60 bg-gradient-to-b from-indigo-50/50 to-white/50">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-indigo-100 to-purple-100 flex items-center justify-center">
                          <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        </div>
                        <span>Title</span>
                      </div>
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-800 uppercase tracking-wide border-r border-gray-200/60 bg-gradient-to-b from-yellow-50/50 to-white/50">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-yellow-100 to-orange-100 flex items-center justify-center">
                          <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 11l7-7 7 7M5 19l7-7 7 7" />
                          </svg>
                        </div>
                        <span>Priority</span>
                      </div>
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-800 uppercase tracking-wide border-r border-gray-200/60 bg-gradient-to-b from-green-50/50 to-white/50">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-green-100 to-emerald-100 flex items-center justify-center">
                          <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <span>Status</span>
                      </div>
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-800 uppercase tracking-wide bg-gradient-to-b from-blue-50/50 to-white/50">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-blue-100 to-cyan-100 flex items-center justify-center">
                          <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                        </div>
                        <span>Due Date</span>
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200/60 bg-white/90 backdrop-blur-sm">
                  {tasks.map((task, index) => (
                    <tr
                      key={task.id}
                      className="hover:bg-gradient-to-r hover:from-indigo-50/60 hover:to-purple-50/60 transition-all duration-300 animate-fade-in border-b border-gray-100/60 hover:shadow-md hover:shadow-gray-200/50"
                      style={{ animationDelay: `${index * 0.1}s` }}
                    >
                      <td className="px-6 py-6 border-r border-gray-200/50">
                        <div className="font-bold text-gray-900 text-lg mb-1">{task.title}</div>
                        {task.description && (
                          <div className="text-sm text-gray-600 mt-2 line-clamp-2 bg-gray-50 p-3 rounded-lg">
                            {task.description}
                          </div>
                        )}
                      </td>
                      <td className="px-6 py-6 border-r border-gray-200/50">
                        <div className="flex items-center justify-center">
                          <span className={`px-5 py-2.5 rounded-2xl text-sm font-bold shadow-lg ${getPriorityClass(task.priority)}`}>
                            {task.priority.toUpperCase()}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-6 border-r border-gray-200/50">
                        <div className="flex items-center justify-center">
                          <span className={`px-5 py-2.5 rounded-2xl text-sm font-bold shadow-lg ${getStatusClass(task.completed)}`}>
                            {task.completed ? 'COMPLETED' : 'PENDING'}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-6 text-gray-700">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-100 to-cyan-100 flex items-center justify-center shadow-sm">
                            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                          </div>
                          <div>
                            <span className="text-sm font-medium block">
                              {task.due_date
                                ? new Date(task.due_date).toLocaleDateString('en-US', {
                                    month: 'short',
                                    day: 'numeric',
                                    year: 'numeric'
                                  })
                                : 'No due date'}
                            </span>
                            {task.due_date && (
                              <div className="w-24 h-1 bg-gray-200 rounded-full mt-1 overflow-hidden">
                                <div
                                  className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full"
                                  style={{
                                    width: `${Math.max(10, 100 - ((new Date(task.due_date).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24 * 30)) * 10)}%`
                                  }}
                                ></div>
                              </div>
                            )}
                          </div>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Chat Interface */}
        <NewChatInterface userId={state.user?.id || ''} isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />

        {/* Chat Bot Icon */}
        <NewChatBotIcon onClick={toggleChat} />
      </div>
    </ProtectedRoute>
  );
}