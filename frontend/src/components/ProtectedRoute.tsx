'use client';

import React, { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { state } = useAuth();
  const router = useRouter();

  // Check if token is expired
  const isTokenExpired = () => {
    if (!state.token) return true;

    try {
      const tokenParts = state.token.split('.');
      if (tokenParts.length !== 3) return true;

      const payload = JSON.parse(atob(tokenParts[1]));
      const currentTime = Math.floor(Date.now() / 1000);

      return payload.exp && payload.exp < currentTime;
    } catch (error) {
      return true;
    }
  };

  // Check authentication status on component mount
  useEffect(() => {
    // If no token in context state, check localStorage
    if (!state.token) {
      const tokenFromStorage = localStorage.getItem('auth_token');
      if (tokenFromStorage) {
        // Token exists in localStorage but not in context - this can happen during navigation
        // The AuthProvider should handle loading this, so we wait a bit to see if it loads
        const timer = setTimeout(() => {
          // If still no token after waiting briefly, redirect to login
          if (!state.token) {
            router.push('/login');
          }
        }, 100);
        return () => clearTimeout(timer);
      } else {
        // No token anywhere, redirect to login
        router.push('/login');
      }
    } else if (isTokenExpired()) {
      // Token in state is expired
      localStorage.removeItem('auth_token');
      router.push('/login');
    }
  }, [state.token, router]);

  // If we don't have a token yet but there might be one in localStorage, show loading
  if (!state.token) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  // If token is expired
  if (isTokenExpired()) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Redirecting to login...</p>
      </div>
    );
  }

  return <>{children}</>;
}