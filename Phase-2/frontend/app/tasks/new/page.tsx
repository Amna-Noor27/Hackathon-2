"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedLayout from '@/components/layout/ProtectedLayout';
import TaskForm from '@/components/tasks/TaskForm';
import { TaskCreate } from '@/types/task';
import { useTasks } from '@/hooks/useTasks';

export default function NewTaskPage() {
  const router = useRouter();
  const { createTask } = useTasks();
  const [error, setError] = useState<string | null>(null);

  const handleCreateTask = async (taskData: TaskCreate) => {
    const success = await createTask(taskData);
    if (success) {
      router.push('/tasks');
      router.refresh();
    } else {
      setError('Failed to create task. Please try again.');
    }
  };

  const handleCancel = () => {
    router.back();
  };

  return (
    <ProtectedLayout>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Create New Task</h1>

          {error && (
            <div className="mb-6 p-4 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          <TaskForm
            onSubmit={handleCreateTask}
            onCancel={handleCancel}
            submitButtonText="Create Task"
          />
        </div>
      </div>
    </ProtectedLayout>
  );
}