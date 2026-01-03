'use client';

import React from 'react';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function SettingsPage() {
  const { state } = useAuth();

  return (
    <ProtectedRoute>
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold mb-8">Settings</h1>

          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Account Information</h2>

            <div className="mb-6">
              <label className="block text-gray-700 font-medium mb-2">Name</label>
              <p className="text-gray-900">{state.user?.name}</p>
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 font-medium mb-2">Email</label>
              <p className="text-gray-900">{state.user?.email}</p>
            </div>

            <div className="flex justify-end">
              <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Update Profile
              </button>
            </div>
          </div>

          <div className="bg-white shadow rounded-lg p-6 mt-6">
            <h2 className="text-xl font-semibold mb-4">Security</h2>

            <div className="mb-6">
              <label className="block text-gray-700 font-medium mb-2">Password</label>
              <p className="text-gray-900">********</p>
            </div>

            <div className="flex justify-end">
              <button className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">
                Change Password
              </button>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}