"use client";

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import ProtectedLayout from '@/components/layout/ProtectedLayout';
import { Task } from '@/types/task';
import { useTasks } from '@/hooks/useTasks';

export default function TaskDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { tasks, fetchTasks, updateTask, deleteTask } = useTasks();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({ title: '', description: '', completed: false });

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  useEffect(() => {
    if (tasks.length > 0) {
      const foundTask = tasks.find(t => t.id === id);
      if (foundTask) {
        setTask(foundTask);
        setEditData({
          title: foundTask.title,
          description: foundTask.description || '',
          completed: foundTask.completed
        });
        setLoading(false);
      } else {
        setError('Task not found');
        setLoading(false);
      }
    }
  }, [tasks, id]);

  const handleToggleCompletion = async () => {
    if (!task) return;

    const success = await updateTask(task.id, { ...task, completed: !task.completed });
    if (!success) {
      setError('Failed to update task. Please try again.');
    }
  };

  const handleEditToggle = async () => {
    if (isEditing && task) {
      // Save changes
      const success = await updateTask(task.id, editData as any);
      if (success) {
        setIsEditing(false);
      } else {
        setError('Failed to update task. Please try again.');
      }
    } else {
      setIsEditing(true);
    }
  };

  const handleDelete = async () => {
    if (!task) return;

    if (window.confirm('Are you sure you want to delete this task?')) {
      const success = await deleteTask(task.id);
      if (success) {
        router.push('/tasks');
      } else {
        setError('Failed to delete task. Please try again.');
      }
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setEditData(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEditData(prev => ({ ...prev, completed: e.target.checked }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-300">Loading task...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 max-w-md w-full text-center">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Error</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">{error}</p>
          <button
            onClick={() => router.push('/tasks')}
            className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Back to Tasks
          </button>
        </div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 max-w-md w-full text-center">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Task Not Found</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">The requested task could not be found.</p>
          <button
            onClick={() => router.push('/tasks')}
            className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Back to Tasks
          </button>
        </div>
      </div>
    );
  }

  return (
    <ProtectedLayout>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              {isEditing ? 'Edit Task' : 'Task Details'}
            </h1>
            <div className="flex space-x-2">
              <button
                onClick={handleEditToggle}
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
              >
                {isEditing ? 'Save' : 'Edit'}
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-800 dark:hover:text-red-400 transition-colors"
              >
                Delete
              </button>
            </div>
          </div>

          <div className="p-6">
            {isEditing ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Title
                  </label>
                  <input
                    type="text"
                    name="title"
                    value={editData.title}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Description
                  </label>
                  <textarea
                    name="description"
                    value={editData.description}
                    onChange={handleInputChange}
                    rows={4}
                    className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                  />
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    name="completed"
                    checked={editData.completed}
                    onChange={handleCheckboxChange}
                    className="h-4 w-4 text-indigo-600 rounded focus:ring-indigo-500"
                  />
                  <label className="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                    Mark as completed
                  </label>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="flex items-start">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={handleToggleCompletion}
                    className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500 mt-1"
                  />
                  <div className="ml-4">
                    <h2 className={`text-xl font-semibold ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900 dark:text-white'}`}>
                      {task.title}
                    </h2>
                    {task.description && (
                      <p className={`mt-2 ${task.completed ? 'text-gray-400 line-through' : 'text-gray-600 dark:text-gray-300'}`}>
                        {task.description}
                      </p>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Created</h3>
                    <p className="mt-1 text-sm text-gray-900 dark:text-white">
                      {new Date(task.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Status</h3>
                    <p className={`mt-1 text-sm font-medium ${task.completed ? 'text-green-600' : 'text-yellow-600'}`}>
                      {task.completed ? 'Completed' : 'Pending'}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </ProtectedLayout>
  );
}