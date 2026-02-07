interface EmptyStateProps {
  title: string;
  description: string;
  icon?: string;
  action?: () => void;
  actionText?: string;
}

export default function EmptyState({
  title,
  description,
  icon = "📝",
  action,
  actionText
}: EmptyStateProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-12 text-center">
      <div className="text-5xl mb-4">{icon}</div>
      <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-300 mb-4">{description}</p>
      {action && actionText && (
        <button
          onClick={action}
          className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
        >
          {actionText}
        </button>
      )}
    </div>
  );
}