'use client';

import React from 'react';
import Header from '@/components/Header';
import { ReactNode } from 'react';

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <>
      <Header />
      <div className="min-h-screen bg-gray-50">
        {children}
      </div>
    </>
  );
}