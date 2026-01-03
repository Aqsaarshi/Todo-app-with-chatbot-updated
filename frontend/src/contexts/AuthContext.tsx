'use client';

import React, { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export interface User {
  id: string
  email: string
  name?: string
}


interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

interface AuthAction {
  type: string;
  payload?: any;
}

interface AuthContextType {
  state: AuthState;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

const initialState: AuthState = {
  user: null,
  token: null,
  loading: false,
  error: null,
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'AUTH_START':
      return { ...state, loading: true, error: null };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        loading: false,
        user: action.payload.user,
        token: action.payload.token,
        error: null
      };
    case 'AUTH_ERROR':
      return { ...state, loading: false, error: action.payload };
    case 'LOGOUT':
      return { ...state, user: null, token: null };
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    default:
      return state;
  }
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const router = useRouter();

  // Check for existing token on initial load and validate it
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      // Decode the token to get user info and check expiration
      try {
        // Simple JWT decoding to get user data from token
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));

          // Check if token is expired
          const currentTime = Math.floor(Date.now() / 1000);
          if (payload.exp && payload.exp < currentTime) {
            console.log('Token has expired');
            localStorage.removeItem('auth_token');
            return;
          }

          const user = {
            id: payload.sub,
            email: payload.email,
            name: payload.email.split('@')[0]
          };

          dispatch({
            type: 'AUTH_SUCCESS',
            payload: {
              user: user,
              token: token
            }
          });
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        // If there's an error decoding the token, remove it
        localStorage.removeItem('auth_token');
      }
    }
  }, []);

  const login = async (email: string, password: string) => {
    dispatch({ type: 'AUTH_START' });

    try {
      // Construct URL with query parameters
      const url = new URL(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`);
      url.searchParams.append('email', email);
      url.searchParams.append('password', password);

      const response = await fetch(url.toString(), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      // Save token to localStorage
      localStorage.setItem('auth_token', data.token);

      // Set user in context
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user: { id: data.user_id, email, name: email.split('@')[0] },
          token: data.token,
        },
      });

      router.push('/dashboard');
    } catch (error: any) {
      dispatch({
        type: 'AUTH_ERROR',
        payload: error.message || 'Login failed',
      });
    }
  };

  const register = async (name: string, email: string, password: string) => {
    dispatch({ type: 'AUTH_START' });

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          name,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      // Save token to localStorage
      localStorage.setItem('auth_token', data.token);

      // Set user in context
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user: { id: data.user_id, email, name },
          token: data.token,
        },
      });

      router.push('/dashboard');
    } catch (error: any) {
      dispatch({
        type: 'AUTH_ERROR',
        payload: error.message || 'Registration failed',
      });
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    dispatch({ type: 'LOGOUT' });
    router.push('/');
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value = {
    state,
    login,
    register,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};