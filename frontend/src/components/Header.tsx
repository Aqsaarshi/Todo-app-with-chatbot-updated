'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';

export default function Header() {
  const { state, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="bg-white/95 backdrop-blur-md sticky top-0 z-50 shadow-md border-b">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        {/* Logo */}
        <Link href="/" className="text-2xl font-bold text-gray-800">
          TodoHub
        </Link>

        {/* Hamburger (Mobile) */}
        <button
          className="md:hidden text-2xl"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          ☰
        </button>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-6 font-medium">
          {state.token ? (
            <>
              <Link href="/dashboard" className="hover:text-gray-600">
                Dashboard
              </Link>
              <Link href="/tasks" className="hover:text-gray-600">
                Tasks
              </Link>

              {/* User Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setMenuOpen(!menuOpen)}
                  className="flex items-center gap-1"
                >
                  {state.user?.name}
                  <span className={menuOpen ? 'rotate-180' : ''}>▼</span>
                </button>

                {menuOpen && (
                  <div className="absolute right-0 mt-2 w-40 bg-white rounded-lg shadow border">
                    <Link
                      href="/settings"
                      className="block px-4 py-2 hover:bg-gray-100"
                      onClick={() => setMenuOpen(false)}
                    >
                      Settings
                    </Link>
                    <button
                      onClick={logout}
                      className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50"
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              <Link href="/login">Login</Link>
              <Link href="/register" className="border px-4 py-1 rounded-full">
                Sign Up
              </Link>
            </>
          )}
        </nav>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="md:hidden px-6 pb-4 space-y-3">
          {state.token ? (
            <>
              <Link href="/dashboard" onClick={() => setMobileOpen(false)}>
                Dashboard
              </Link>
              <Link href="/tasks" onClick={() => setMobileOpen(false)}>
                Tasks
              </Link>
              <Link href="/settings" onClick={() => setMobileOpen(false)}>
                Settings
              </Link>
              <button
                onClick={logout}
                className="block text-red-600"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login">Login</Link>
              <Link href="/register">Sign Up</Link>
            </>
          )}
        </div>
      )}
    </header>
  );
}
