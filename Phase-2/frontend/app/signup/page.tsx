"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import RegisterForm from '@/components/auth/RegisterForm';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const { checkAuthStatus } = useAuth();
  const router = useRouter();

  // If user is already authenticated, redirect to tasks
  useEffect(() => {
    if (checkAuthStatus()) {
      router.push('/tasks');
    }
  }, [checkAuthStatus, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl w-full max-w-md p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Create Account</h1>
          <p className="text-gray-600 dark:text-gray-300">Join TodoApp today - it's free!</p>
        </div>

        <RegisterForm />

        <div className="mt-6 text-center">
          <p className="text-gray-600 dark:text-gray-400">
            Already have an account?{" "}
            <Link href="/login" className="text-indigo-600 dark:text-indigo-400 font-medium hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}