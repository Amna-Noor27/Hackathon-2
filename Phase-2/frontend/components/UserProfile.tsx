'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { User as UserType } from '@/types/auth';

interface UserProfileProps {
  className?: string;
}

const UserProfile: React.FC<UserProfileProps> = ({ className = '' }) => {
  const { user, loading } = useAuth();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    // Get user email from localStorage
    const storedEmail = localStorage.getItem('userEmail');
    setUserEmail(storedEmail);
  }, []);

  const handleLogout = async () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    window.location.href = '/login';
  };

  if (loading) {
    return (
      <div className={`flex items-center space-x-3 ${className}`}>
        <div className="animate-pulse bg-gray-200 rounded-full w-8 h-8"></div>
        <span className="text-sm font-medium text-gray-500">Loading...</span>
      </div>
    );
  }

  // If we have a stored email in localStorage, use that instead of the auth user
  const displayName = userEmail || user?.email || 'User';

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <div className="relative">
        <div className="bg-indigo-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-semibold cursor-pointer"
             onClick={() => setShowDropdown(!showDropdown)}>
          {displayName.charAt(0).toUpperCase()}
        </div>

        {/* Dropdown menu */}
        {showDropdown && (
          <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 z-50">
            <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-700">
              <p className="text-sm font-medium text-gray-900 dark:text-white truncate">{displayName}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{userEmail || user?.email || 'No email'}</p>
            </div>
            <button
              onClick={handleLogout}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              Sign out
            </button>
          </div>
        )}

        {!showDropdown && (
          <div className="absolute bottom-0 right-0 w-2 h-2 bg-green-500 rounded-full border border-white"></div>
        )}
      </div>
      <div className="hidden md:block">
        <p className="text-sm font-medium text-gray-900 dark:text-white">{displayName}</p>
        <p className="text-xs text-gray-500 dark:text-gray-400">{userEmail || user?.email || 'No email'}</p>
      </div>
    </div>
  );
};

export default UserProfile;