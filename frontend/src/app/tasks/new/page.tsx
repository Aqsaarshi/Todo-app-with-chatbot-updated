'use client';

import React from 'react';
import Header from '@/components/Header';
import TaskForm from '@/components/TaskForm';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function NewTaskPage() {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <Header />
        <div className="container mx-auto px-4 py-16">
          <div className="mb-10 text-center">
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
              Create New Task
            </h1>
            <p className="text-gray-600 text-lg">
              Fill out the form below to add a new task to your list
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-10 border border-gray-200/50 transform hover:scale-[1.01] transition-transform duration-300">
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                  <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Task Details
                </h2>
                <p className="text-gray-600">
                  Enter the details for your new task below. All fields are designed to help you organize your work effectively.
                </p>
              </div>

              <div className="border-t border-gray-200/50 pt-8">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center gap-3">
                  <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Add Your Task
                </h3>
                <TaskForm />
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
