"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { loading, checkAuthStatus, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    const checkAuth = () => {
      // Check both the auth hook state and localStorage token
      const hasBetterAuthSession = checkAuthStatus();
      const hasLocalStorageToken = !!localStorage.getItem('token');
      const isLoggedIn = hasBetterAuthSession || hasLocalStorageToken;

      if (!loading && !isLoggedIn) {
        router.push('/login');
      }
    };

    checkAuth();
  }, [loading, checkAuthStatus, user, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-300">Checking authentication...</p>
        </div>
      </div>
    );
  }

  // Check both the auth hook state and localStorage token
  const hasBetterAuthSession = checkAuthStatus();
  const hasLocalStorageToken = !!localStorage.getItem('token');
  const isLoggedIn = hasBetterAuthSession || hasLocalStorageToken;

  if (!isLoggedIn) {
    // Show loading state briefly while redirect happens
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-2 text-gray-600 dark:text-gray-300">Redirecting...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}