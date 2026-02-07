import { useState, useEffect } from 'react';
import { Task, TaskCreate, TaskUpdate } from '@/types/task';

interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: TaskCreate) => Promise<boolean>;
  updateTask: (id: string, taskData: TaskUpdate) => Promise<boolean>;
  deleteTask: (id: string) => Promise<boolean>;
  toggleTaskCompletion: (id: string) => Promise<boolean>;
}

export function useTasks(): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);

      // Get token directly from localStorage
      const token = localStorage.getItem('token');

      // Check if token exists
      if (!token) {
        // Redirect to login if no token is found
        window.location.href = '/login';
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://noormusarrat-full-stack-todoapp.hf.space'}/api/tasks`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies for authentication
      });

      if (response.status === 401) {
        // Unauthorized - token might be expired
        // Dispatch unauthorized event to trigger cleanup in AuthProvider
        window.dispatchEvent(new Event('unauthorized'));
        return;
      }

      if (!response.ok) {
        throw new Error(`Failed to fetch tasks: ${response.statusText}`);
      }

      const data: Task[] = await response.json();
      setTasks(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (taskData: TaskCreate): Promise<boolean> => {
    try {
      setError(null);

      // Get token directly from localStorage
      const token = localStorage.getItem('token');

      // Check if token exists
      if (!token) {
        // Redirect to login if no token is found
        window.location.href = '/login';
        return false;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://noormusarrat-full-stack-todoapp.hf.space'}/api/tasks`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
        credentials: 'include', // Include cookies for authentication
      });

      if (response.status === 401) {
        // Dispatch unauthorized event to trigger cleanup in AuthProvider
        window.dispatchEvent(new Event('unauthorized'));
        return false;
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create task');
      }

      const newTask: Task = await response.json();
      setTasks([...tasks, newTask]);
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('Error creating task:', err);
      return false;
    }
  };

  const updateTask = async (id: string, taskData: TaskUpdate): Promise<boolean> => {
    try {
      setError(null);

      // Get token directly from localStorage
      const token = localStorage.getItem('token');

      // Check if token exists
      if (!token) {
        // Redirect to login if no token is found
        window.location.href = '/login';
        return false;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://noormusarrat-full-stack-todoapp.hf.space'}/api/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
        credentials: 'include', // Include cookies for authentication
      });

      if (response.status === 401) {
        // Dispatch unauthorized event to trigger cleanup in AuthProvider
        window.dispatchEvent(new Event('unauthorized'));
        return false;
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update task');
      }

      const updatedTask: Task = await response.json();
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('Error updating task:', err);
      return false;
    }
  };

  const deleteTask = async (id: string): Promise<boolean> => {
    try {
      setError(null);

      // Get token directly from localStorage
      const token = localStorage.getItem('token');

      // Check if token exists
      if (!token) {
        // Redirect to login if no token is found
        window.location.href = '/login';
        return false;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://noormusarrat-full-stack-todoapp.hf.space'}/api/tasks/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        credentials: 'include', // Include cookies for authentication
      });

      if (response.status === 401) {
        // Dispatch unauthorized event to trigger cleanup in AuthProvider
        window.dispatchEvent(new Event('unauthorized'));
        return false;
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete task');
      }

      setTasks(tasks.filter(task => task.id !== id));
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('Error deleting task:', err);
      return false;
    }
  };

  const toggleTaskCompletion = async (id: string): Promise<boolean> => {
    const task = tasks.find(t => t.id === id);
    if (!task) return false;

    return updateTask(id, { ...task, completed: !task.completed });
  };

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
}