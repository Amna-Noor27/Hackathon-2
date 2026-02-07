import { Task } from '@/types/task';

interface TaskCardProps {
  task: Task;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export default function TaskCard({ task, onToggle, onDelete }: TaskCardProps) {
  return (
    <div
      className={`bg-white dark:bg-gray-800 rounded-xl shadow p-6 flex items-start ${
        task.completed ? "opacity-70" : ""
      }`}
    >
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggle(task.id)}
        className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500 mt-0.5"
      />
      <div className="ml-4 flex-1">
        <h3
          className={`text-lg font-medium ${
            task.completed
              ? "text-gray-500 dark:text-gray-400 line-through"
              : "text-gray-900 dark:text-white"
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p
            className={`mt-1 ${
              task.completed
                ? "text-gray-400 dark:text-gray-500 line-through"
                : "text-gray-600 dark:text-gray-300"
            }`}
          >
            {task.description}
          </p>
        )}
        <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
          Created: {new Date(task.created_at).toLocaleString()}
        </div>
      </div>
      <button
        onClick={() => onDelete(task.id)}
        className="text-red-500 hover:text-red-700 dark:hover:text-red-400 ml-4"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
          />
        </svg>
      </button>
    </div>
  );
}