'use client';

import React, { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Header from '@/components/Header';
import NewChatBotIcon from '@/components/NewChatBotIcon';
import NewChatInterface from '@/components/NewChatInterface';

export default function HomePage() {
  const { state: authState } = useAuth();
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  // Use a default user ID if not authenticated, or show a message
  const userId = authState.user?.id || 'anonymous';

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <Header />

      {/* Hero Section with enhanced animations */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center animate-fade-in">
          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6 leading-tight">
            Manage Your Tasks Effortlessly
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
            A simple and powerful todo application to help you organize your life and boost productivity.
          </p>

          {/* Animated CTA buttons */}
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6 animate-fade-in">
            <a
              href="/register"
              className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl group relative overflow-hidden"
            >
              <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
              <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Get Started
              </span>
            </a>
            <a
              href="/login"
              className="bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl group relative overflow-hidden"
            >
              <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
              <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
                <svg className="w-5 h-5 group-hover:-translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                Sign In
              </span>
            </a>
          </div>
        </div>

        {/* Features Section with staggered animations */}
        <div className="mt-20 max-w-6xl mx-auto bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-white/20 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div
              className="text-center group animate-slide-in-left"
              style={{ animationDelay: '0.1s' }}
            >
              <div className="bg-gradient-to-br from-blue-100 to-indigo-100 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">Task Management</h3>
              <p className="text-gray-600 leading-relaxed">Create, update, and organize your tasks with ease using our intuitive interface.</p>
            </div>

            <div
              className="text-center group animate-slide-in-up"
              style={{ animationDelay: '0.2s' }}
            >
              <div className="bg-gradient-to-br from-green-100 to-emerald-100 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">Secure & Private</h3>
              <p className="text-gray-600 leading-relaxed">Your data is protected with industry-standard security measures and encryption.</p>
            </div>

            <div
              className="text-center group animate-slide-in-right"
              style={{ animationDelay: '0.3s' }}
            >
              <div className="bg-gradient-to-br from-purple-100 to-violet-100 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">Fully Responsive</h3>
              <p className="text-gray-600 leading-relaxed">Access your tasks from any device, anywhere with our seamless responsive design.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Interface */}
      <NewChatInterface userId={authState.user?.id || 'anonymous'} isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
      {/* Chat Bot Icon */}
      <NewChatBotIcon onClick={toggleChat} />
    </div>
  );
}