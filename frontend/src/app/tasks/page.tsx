'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Header from '@/components/Header';
import TaskFilterBar from '@/components/TaskFilterBar';
import { tasksAPI } from '@/lib/api/tasks';
import NewChatBotIcon from '@/components/NewChatBotIcon';
import NewChatInterface from '@/components/NewChatInterface';

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

export default function TasksPage() {
  const { state } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [filters, setFilters] = useState({
    completed: '',
    priority: '',
    sort: 'created_at',
    order: 'desc'
  });
  const [error, setError] = useState<string | null>(null);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  useEffect(() => {
    if (state.token && state.user?.id && state.user.id !== 'undefined') {
      fetchTasks();
    }
  }, [filters, state.token, state.user?.id]);

  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'taskDeleted') fetchTasks();
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [state.token, state.user?.id, filters]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('auth_token');
      const userId = state.user?.id;
      if (!token || !userId) throw new Error('User not authenticated');

      // Use the correct API function from tasksAPI
      const response = await tasksAPI.getTasks(userId, token, {
        completed: filters.completed || undefined,
        priority: filters.priority || undefined,
        sort: filters.sort,
        order: filters.order,
      });

      setTasks(response);
    } catch (err: any) {
      console.error('Error fetching tasks:', err);
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId: string, currentStatus: boolean) => {
    try {
      const token = localStorage.getItem('auth_token');
      const userId = state.user?.id;
      if (!token || !userId) throw new Error('User not authenticated');

      const updatedTask = await tasksAPI.updateTask(userId, taskId, token, { completed: !currentStatus });
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
    } catch (error: any) {
      console.error('Error updating task:', error);
      alert('Error updating task: ' + error.message);
    }
  };

  const deleteTask = async (taskId: string) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    try {
      const token = localStorage.getItem('auth_token');
      const userId = state.user?.id;
      if (!token || !userId) throw new Error('User not authenticated');

      await tasksAPI.deleteTask(userId, taskId, token);
      setTasks(tasks.filter(task => task.id !== taskId));
      window.dispatchEvent(new CustomEvent('taskDeleted'));
      localStorage.setItem('taskDeleted', Date.now().toString());
    } catch (error: any) {
      console.error('Error deleting task:', error);
      alert('Error deleting task: ' + error.message);
    }
  };

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleClearFilters = () => setFilters({ completed: '', priority: '', sort: 'created_at', order: 'desc' });

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
        <Header />

        <div className="container mx-auto px-4 py-8">
          {/* Top bar with enhanced styling */}
          <div className="flex flex-col lg:flex-row justify-between items-center gap-8 mb-10 animate-fade-in">
            <div className="text-center lg:text-left">
              <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                Your Tasks
              </h1>
              <p className="text-gray-600 text-lg">
                {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} in your list
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4">
              <a
                href="/tasks/new"
                className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-2xl shadow-xl transition-all duration-300 transform hover:scale-105 hover:shadow-2xl group relative overflow-hidden flex items-center justify-center gap-3"
              >
                <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                <span className="relative flex items-center gap-3 group-hover:gap-4 transition-all duration-300">
                  <svg className="w-6 h-6 group-hover:rotate-12 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  <span className="text-lg font-semibold">Add New Task</span>
                </span>
              </a>

              {/* Stats Card */}
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-gray-200/50 min-w-48">
                <h3 className="font-semibold text-gray-700 mb-2">Progress</h3>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-green-100 to-blue-100 flex items-center justify-center">
                    <span className="text-2xl font-bold text-blue-600">
                      {tasks.length > 0 ? Math.round((tasks.filter(t => t.completed).length / tasks.length) * 100) : 0}%
                    </span>
                  </div>
                  <div className="text-sm">
                    <div className="text-green-600 font-medium">
                      {tasks.filter(t => t.completed).length} done
                    </div>
                    <div className="text-gray-500">
                      {tasks.length - tasks.filter(t => t.completed).length} pending
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-2xl mb-8 animate-fade-in backdrop-blur-sm">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <p className="text-red-700 font-medium text-lg">{error}</p>
                  <button
                    onClick={fetchTasks}
                    className="mt-3 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-medium py-2 px-6 rounded-xl transition-all duration-300 transform hover:scale-105"
                  >
                    Retry
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Filters */}
          <TaskFilterBar
            completedFilter={filters.completed}
            priorityFilter={filters.priority}
            sortField={filters.sort}
            sortOrder={filters.order}
            onCompletedChange={(v) => setFilters(prev => ({ ...prev, completed: v }))}
            onPriorityChange={(v) => setFilters(prev => ({ ...prev, priority: v }))}
            onSortFieldChange={(v) => setFilters(prev => ({ ...prev, sort: v }))}
            onSortOrderChange={(v) => setFilters(prev => ({ ...prev, order: v }))}
            onClearFilters={() => setFilters({ completed: '', priority: '', sort: 'created_at', order: 'desc' })}
          />

          {/* Tasks Grid */}
          {loading ? (
            <div className="flex justify-center items-center py-20">
              <div className="spinner"></div>
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-16 animate-fade-in">
              <div className="mx-auto w-32 h-32 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-8">
                <svg className="w-16 h-16 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-gray-600 text-xl mb-6">
                No tasks found. Create your first task or adjust filters!
              </p>
              <a href="/tasks/new" className="btn-primary inline-flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Create Your First Task
              </a>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in">
              {tasks.map((task, index) => (
                <div
                  key={task.id}
                  className={`card p-6 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl border-l-4 ${
                    task.completed ? 'border-green-500' : 'border-blue-500'
                  } animate-fade-in`}
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="flex justify-between items-start mb-4">
                    <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                      {task.title}
                    </h3>
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => toggleTaskCompletion(task.id, task.completed)}
                      className="h-6 w-6 text-blue-600 rounded-full border-2 border-gray-300 focus:ring-blue-500 focus:ring-2 cursor-pointer"
                      title="Toggle completion"
                    />
                  </div>

                  {task.description && (
                    <p className="text-gray-600 mb-6 leading-relaxed">
                      {task.description}
                    </p>
                  )}

                  <div className="flex flex-wrap gap-3 items-center justify-between mb-6">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      task.priority === 'high' ? 'bg-red-200 text-red-800' :
                      task.priority === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                      'bg-green-200 text-green-800'
                    }`}>
                      {task.priority}
                    </span>

                    {task.due_date && (
                      <span className="text-sm text-gray-500 flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Due: {new Date(task.due_date).toLocaleDateString()}
                      </span>
                    )}
                  </div>

                  <div className="flex justify-between items-center pt-4 border-t border-gray-100">
                    <a href={`/tasks/${task.id}`} className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-medium text-sm rounded-lg px-3 py-1.5 transition-all duration-300 transform hover:scale-105 group relative overflow-hidden">
                      <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                      <span className="relative flex items-center gap-1 group-hover:gap-2 transition-all duration-300">
                        <svg className="w-4 h-4 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        View
                      </span>
                    </a>
                    <a href={`/tasks/edit/${task.id}`} className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-medium text-sm rounded-lg px-3 py-1.5 transition-all duration-300 transform hover:scale-105 group relative overflow-hidden">
                      <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                      <span className="relative flex items-center gap-1 group-hover:gap-2 transition-all duration-300">
                        <svg className="w-4 h-4 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                        Edit
                      </span>
                    </a>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white font-medium text-sm rounded-lg px-3 py-1.5 transition-all duration-300 transform hover:scale-105 group relative overflow-hidden"
                    >
                      <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
                      <span className="relative flex items-center gap-1 group-hover:gap-2 transition-all duration-300">
                        <svg className="w-4 h-4 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Delete
                      </span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Chat Interface */}
        <NewChatInterface userId={state.user?.id || ''} isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />

        {/* Chat Bot Icon */}
        <NewChatBotIcon onClick={toggleChat} />
      </div>
    </ProtectedRoute>
  );
}
