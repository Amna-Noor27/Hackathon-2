'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export default function Sidebar() {
  const { user, logout, loading } = useAuth();

  return (
    <aside className="w-64 bg-white dark:bg-gray-800 shadow-md h-full min-h-screen">
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">TodoApp</h2>
      </div>

      <nav className="p-4">
        <ul className="space-y-2">
          <li>
            <Link
              href="/tasks"
              className="flex items-center p-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <span className="mr-3">📋</span>
              <span>Your Tasks</span>
            </Link>
          </li>
          <li>
            <Link
              href="/profile"
              className="flex items-center p-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <span className="mr-3">👤</span>
              <span>Profile</span>
            </Link>
          </li>
        </ul>
      </nav>

      <div className="absolute bottom-0 w-64 p-4 border-t border-gray-200 dark:border-gray-700">
        {loading ? (
          <div className="flex items-center">
            <div className="animate-pulse bg-gray-200 rounded-full w-10 h-10"></div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-900 dark:text-white">Loading...</p>
            </div>
          </div>
        ) : user ? (
          <div className="flex items-center">
            <div className="bg-indigo-500 text-white rounded-full w-10 h-10 flex items-center justify-center font-semibold">
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-900 dark:text-white">{user.name}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 truncate max-w-[120px]">{user.email}</p>
              <button
                onClick={logout}
                className="mt-1 text-xs text-indigo-600 dark:text-indigo-400 hover:underline"
              >
                Sign out
              </button>
            </div>
          </div>
        ) : (
          <div className="text-sm text-gray-500 dark:text-gray-400">
            <p>Not signed in</p>
            <Link href="/login" className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline mt-1 block">
              Sign in
            </Link>
          </div>
        )}
      </div>
    </aside>
  );
}