"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import ProtectedLayout from '@/components/layout/ProtectedLayout';
import TaskForm from '@/components/tasks/TaskForm';
import TaskList from '@/components/tasks/TaskList';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import ErrorDisplay from '@/components/ui/ErrorDisplay';
import { Task } from '@/types/task';
import { useTasks } from '@/hooks/useTasks';

export default function TasksPage() {
  const router = useRouter();
  const {
    tasks,
    loading,
    error: hookError,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion
  } = useTasks();

  // Fetch tasks on mount (ProtectedRoute handles auth check)
  useEffect(() => {
    fetchTasks();
  }, []); // Empty dependency array to run only once on mount

  const [error, setError] = useState<string | null>(null);

  const handleAddTask = async (taskData: { title: string; description?: string }) => {
    // Only send the fields that the backend expects, without user_id
    const taskPayload = {
      title: taskData.title,
      description: taskData.description,
      completed: false
    };
    const success = await createTask(taskPayload);
    if (!success) {
      setError('Failed to create task. Please try again.');
    }
  };

  const handleToggleTask = async (taskId: string) => {
    const success = await toggleTaskCompletion(taskId);
    if (!success) {
      setError('Failed to update task. Please try again.');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task? 🧐')) {
      return;
    }

    const success = await deleteTask(taskId);
    if (!success) {
      setError('Failed to delete task. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-gray-600 dark:text-gray-300">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <ProtectedLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Your Tasks</h2>
          <div className="text-sm text-gray-600 dark:text-gray-300">
            {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
          </div>
        </div>

        {(error || hookError) && (
          <div className="mb-6">
            <ErrorDisplay
              message={error || hookError || ''}
              onRetry={() => setError(null)}
              retryText="Dismiss"
            />
          </div>
        )}

        {/* Add Task Form */}
        <TaskForm onSubmit={handleAddTask} submitButtonText="Add Task" />

        {/* Tasks List */}
        <TaskList
          tasks={tasks}
          onToggle={handleToggleTask}
          onDelete={handleDeleteTask}
        />
      </div>
    </ProtectedLayout>
  );
}