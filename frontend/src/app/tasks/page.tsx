'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import Header from '@/components/Header';
import TaskFilterBar from '@/components/TaskFilterBar';
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

export default function TasksPage() {
  const { state } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    completed: '',
    priority: '',
    sort: 'created_at',
    order: 'desc'
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (state.token && state.user?.id && state.user.id !== 'undefined') {
      fetchTasks();
    }
  }, [filters, state.token, state.user?.id]);

  useEffect(() => {
    const handleStorageChange = async (e: StorageEvent) => {
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

      const tasks = await tasksAPI.getTasks(userId, token, {
        completed: filters.completed || undefined,
        priority: filters.priority || undefined,
        sort: filters.sort,
        order: filters.order,
      });

      setTasks(tasks);
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

      const updatedTask = await tasksAPI.toggleTaskCompletion(userId, taskId, token, !currentStatus);
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
      <div className="min-h-screen bg-gray-100">
        <Header />

        <div className="container mx-auto px-4 py-8">
          {/* Top bar */}
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold">Your Tasks</h1>
            <a
              href="/tasks/new"
              className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold py-2 px-4 rounded-xl shadow transition transform hover:scale-105"
            >
              Add New Task
            </a>
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              <p>{error}</p>
              <button
                onClick={fetchTasks}
                className="mt-2 bg-red-500 hover:bg-red-700 text-white py-1 px-3 rounded text-sm"
              >
                Retry
              </button>
            </div>
          )}

          {/* Filters */}
          <TaskFilterBar
            completedFilter={filters.completed}
            priorityFilter={filters.priority}
            sortField={filters.sort}
            sortOrder={filters.order}
            onCompletedChange={(v) => handleFilterChange('completed', v)}
            onPriorityChange={(v) => handleFilterChange('priority', v)}
            onSortFieldChange={(v) => handleFilterChange('sort', v)}
            onSortOrderChange={(v) => handleFilterChange('order', v)}
            onClearFilters={handleClearFilters}
          />

          {/* Tasks Grid */}
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-12 text-gray-600 text-lg">
              No tasks found. Create your first task or adjust filters!
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {tasks.map(task => (
                <div
                  key={task.id}
                  className={`bg-white shadow-md rounded-xl p-6 transition transform hover:-translate-y-1 hover:shadow-xl border-l-4 ${
                    task.completed ? 'border-green-500' : 'border-blue-500'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                      {task.title}
                    </h3>
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => toggleTaskCompletion(task.id, task.completed)}
                      className="h-5 w-5 text-blue-600 rounded"
                      title="Toggle completion"
                    />
                  </div>
                  {task.description && <p className="text-gray-600 mt-2">{task.description}</p>}
                  <div className="mt-4 flex justify-between items-center">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      task.priority === 'high' ? 'bg-red-200 text-red-800' :
                      task.priority === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                      'bg-green-200 text-green-800'
                    }`}>
                      {task.priority}
                    </span>
                    {task.due_date && <span className="text-sm text-gray-500">Due: {new Date(task.due_date).toLocaleDateString()}</span>}
                  </div>
                  <div className="mt-4 flex justify-end space-x-3">
                    <a href={`/tasks/${task.id}`} className="text-blue-600 hover:text-blue-800 text-sm">View</a>
                    <a href={`/tasks/edit/${task.id}`} className="text-green-600 hover:text-green-800 text-sm">Edit</a>
                    <button onClick={() => deleteTask(task.id)} className="text-red-600 hover:text-red-800 text-sm">Delete</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
