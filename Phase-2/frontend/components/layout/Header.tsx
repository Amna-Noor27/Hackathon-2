'use client';

import { ReactNode } from 'react';
import UserProfile from '../UserProfile';

interface HeaderProps {
  children?: ReactNode;
}

export default function Header({ children }: HeaderProps) {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-indigo-600 dark:text-indigo-400">TodoApp</h1>
          </div>
          <div className="flex items-center space-x-4">
            <UserProfile />
            {children}
          </div>
        </div>
      </div>
    </header>
  );
}