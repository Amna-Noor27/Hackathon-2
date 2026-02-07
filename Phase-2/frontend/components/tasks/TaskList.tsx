import { Task } from '@/types/task';
import TaskCard from '@/components/tasks/TaskCard';

interface TaskListProps {
  tasks: Task[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export default function TaskList({ tasks, onToggle, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-12 text-center">
        <div className="text-5xl mb-4">📝</div>
        <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-2">No tasks yet</h3>
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          Get started by adding your first task.
        </p>
        <div className="text-sm text-gray-500 dark:text-gray-400">
          You'll see your tasks appear here once you create them.
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}