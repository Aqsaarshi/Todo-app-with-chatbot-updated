'use client';

import React from 'react';
import Header from '@/components/Header';
import TaskForm from '@/components/TaskForm';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function NewTaskPage() {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <Header />
        <div className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Create New Task</h1>
            <p className="text-gray-600 mt-2">Fill out the form below to add a new task.</p>
          </div>
          <div className="bg-white shadow-md rounded-xl p-6">
            <TaskForm />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
