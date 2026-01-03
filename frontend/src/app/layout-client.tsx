'use client';

import { AuthProvider } from '@/contexts/AuthContext';
import Sidebar from '@/components/Sidebar';
import { ReactNode } from 'react';

export default function LayoutClient({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <div className="flex">
        <Sidebar />
        <main className="flex-1">
          {children}
        </main>
      </div>
    </AuthProvider>
  );
}