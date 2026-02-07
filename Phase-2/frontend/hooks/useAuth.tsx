'use client';

import { createContext, useContext, ReactNode, useEffect, useState } from 'react';
import { useSession } from '@/lib/auth-client';
import { authClient } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';
import { User } from '@/types/auth';

interface Session {
  user: {
    id: string;
    email?: string;
    name?: string;
  };
  session?: {
    createdAt?: string | Date;
    updatedAt?: string | Date;
  };
}

interface AuthContextType {
  user: User | null;
  session: Session | null; // Better Auth session object
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (name: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  checkAuthStatus: () => boolean;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: session, isPending } = useSession();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const router = useRouter();

  // Check for token in localStorage on initial load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(!!user); // Set based on user if no token in localStorage
    }
  }, [user]); // Added user as dependency to update when user changes

  // Set loading to false once we have session data
  useEffect(() => {
    if (!isPending) {
      setLoading(false);
    }
  }, [isPending]);

  useEffect(() => {
    if (session?.user) {
      // Map Better Auth session to our User type
      const sessionUser = session.user;
      if (sessionUser) {
        const mappedUser: User = {
            id: sessionUser.id,
            email: sessionUser.email || '',
            name: sessionUser.name || sessionUser.email?.split('@')[0] || '', // Fallback to email prefix if no name
            created_at: session.session?.createdAt ? new Date(session.session.createdAt).toISOString() : new Date().toISOString(),
            updated_at: session.session?.updatedAt ? new Date(session.session.updatedAt).toISOString() : new Date().toISOString(),
          };

        setUser(mappedUser);

        // Ensure token is stored in localStorage for fallback access
        // This will help ensure tasks API can access the token
        if (session.session?.token) {
          localStorage.setItem('token', session.session.token);
        }
      }
    } else {
      setUser(null);
    }

    // Update loading state when session status is no longer loading
    if (!isPending) {
      setLoading(false);
    }
  }, [session, isPending]);

  const login = async (email: string, password: string): Promise<boolean> => {
    // Debug log to see if the state is capturing the text
    console.log("CLICKED LOGIN WITH:", email, password);

    try {
      setLoading(true);
      setError(null);

      // Log the login data before sending
      console.log("LOGIN DATA BEFORE SENDING:", { email, password });

      // Use dynamic API URL from environment variable
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://noormusarrat-full-stack-todoapp.hf.space';
      // Force-fetch logic to bypass authClient and test backend connectivity
      const response = await fetch(`${API_URL}/api/auth/sign-in/email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.trim(), password: password })
      });
      const result = await response.json();
      console.log("MANUAL FETCH RESULT:", result);

      // Handle the response from the manual fetch
      if (!response.ok) {
        let errorMessage = 'Login failed';
        if (result.detail) {
          errorMessage = result.detail;
        } else if (result.error) {
          errorMessage = typeof result.error === 'string' ? result.error : result.error.message || 'Login failed';
        }
        setError(errorMessage);
        return false;
      }

      // Debug the full response from backend
      console.log("FULL BACKEND RESPONSE:", result);

      // Flexible token capture to handle different possible naming conventions
      const token = result.token || result.access_token || result.sessionToken || result.accessToken;
      if (token) {
        localStorage.setItem('token', token);
        console.log("TOKEN SUCCESSFULLY SAVED!");
      } else {
        console.error("NO TOKEN FOUND IN RESPONSE OBJECT", result);
      }

      console.log("Login successful with manual fetch, redirecting...");

      // Use authClient to sync the session state with Better Auth
      const authResult = await authClient.signIn.email({
        email: email.trim(),
        password: password,
        callbackURL: "/tasks"  // Redirect to tasks after login
      });

      // Flexible token capture for authResult to handle different possible naming conventions
      const authToken = (authResult as any)?.token || (authResult as any)?.data?.token || (authResult as any)?.access_token || (authResult as any)?.data?.access_token || (authResult as any)?.sessionToken || (authResult as any)?.data?.sessionToken || (authResult as any)?.accessToken || (authResult as any)?.data?.accessToken;
      if (authToken) {
        localStorage.setItem('token', authToken);
        console.log("TOKEN SUCCESSFULLY SAVED FROM AUTH RESULT!");
        setIsAuthenticated(true);
        window.location.href = '/tasks'; // Direct redirect to ensure proper navigation
      } else {
        console.error("NO TOKEN FOUND IN AUTH RESULT OBJECT", authResult);
        // Fallback to router if token is not found
        router.push('/tasks');
        router.refresh();
      }
      return true;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'An unexpected error occurred during login';
      setError(errorMessage);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const register = async (name: string, email: string, password: string): Promise<boolean> => {
  try {
    // Validate required fields before making the call
    if (!email || !password) {
      setError('Email and password are required');
      return false;
    }

    setLoading(true);
    setError(null);

    console.log("Sending Signup Data:", { email, password, name });

    // Use dynamic API URL from environment variable
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://noormusarrat-full-stack-todoapp.hf.space';
    const response = await fetch(`${API_URL}/api/auth/sign-up/email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name })
    });

    const result = await response.json();

    if (!response.ok) {
      console.error('Registration error response:', result);
      setError(result.detail || 'Registration failed');
      return false;
    }

    console.log("Full Signup Result:", result);

    // Debug the full response from backend
    console.log("FULL BACKEND RESPONSE:", result);

    // Flexible token capture to handle different possible naming conventions
    const token = result.token || result.access_token || result.sessionToken || result.accessToken;
    if (token) {
      localStorage.setItem('token', token);
      console.log("TOKEN SUCCESSFULLY SAVED!");
      setIsAuthenticated(true);
      window.location.href = '/tasks'; // Direct redirect to ensure proper navigation
    } else {
      console.error("NO TOKEN FOUND IN RESPONSE OBJECT", result);
      // Fallback to router if token is not found
      router.push('/tasks');
      router.refresh();
    }

    return true;
  } catch (error) {
    const errorMessage =
      error instanceof Error ? error.message : 'An unexpected error occurred during registration';
    setError(errorMessage);
    return false;
  } finally {
    setLoading(false);
  }
};


  const logout = async () => {
    try {
      // Set loading to true during logout
      setLoading(true);

      // Use Better Auth's sign out method to clear the session
      await authClient.signOut();

      // Redirect to login page
      router.push('/login');
    } finally {
      // Ensure loading is set to false after logout completes
      setLoading(false);
    }
  };

  const clearError = () => {
    setError(null);
  };

  const checkAuthStatus = (): boolean => {
    // Check both Better Auth session and localStorage token
    const hasBetterAuthSession = !!user && !!session;
    const hasLocalStorageToken = !!localStorage.getItem('token');
    return hasBetterAuthSession || hasLocalStorageToken;
  };

  const value = {
    user,
    session,
    loading,
    error,
    login,
    register,
    logout,
    checkAuthStatus,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}