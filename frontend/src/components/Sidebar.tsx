'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export default function Sidebar() {
  const { state } = useAuth();
  const pathname = usePathname();

  // Only show sidebar when user is authenticated
  if (!state.token) {
    return null;
  }

  const isActive = (path: string) => {
    return pathname === path;
  };

  return (
    <aside className="w-64 bg-gray-800 text-white min-h-screen hidden md:block">
      <div className="p-4">
        <h2 className="text-xl font-semibold">Todo App</h2>
      </div>
      <nav className="mt-6">
        <ul>
          <li>
            <Link
              href="/dashboard"
              className={`flex items-center px-6 py-3 text-sm font-medium ${
                isActive('/dashboard')
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <span>Dashboard</span>
            </Link>
          </li>
          <li>
            <Link
              href="/tasks"
              className={`flex items-center px-6 py-3 text-sm font-medium ${
                isActive('/tasks')
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <span>My Tasks</span>
            </Link>
          </li>
          <li>
            <Link
              href="/tasks/new"
              className={`flex items-center px-6 py-3 text-sm font-medium ${
                isActive('/tasks/new')
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <span>Create Task</span>
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}