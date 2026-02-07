import Link from "next/link";

export default function FeaturesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6 max-w-7xl mx-auto">
        <Link href="/" className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">TodoApp</Link>
        <div className="flex space-x-4">
          <Link
            href="/login"
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
          >
            Login
          </Link>
          <Link
            href="/signup"
            className="px-4 py-2 text-sm font-medium bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
          >
            Sign Up
          </Link>
        </div>
      </nav>

      <main className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Powerful Features</h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Discover everything TodoApp offers to help you stay organized and productive
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            {[
              {
                title: "Smart Organization",
                description: "Intelligent categorization and tagging to keep your tasks organized.",
                icon: "📊",
                details: "Our smart tagging system automatically suggests categories for your tasks based on keywords and context."
              },
              {
                title: "Priority Management",
                description: "Set priorities and deadlines to focus on what matters most.",
                icon: "⚡",
                details: "Easily set priority levels and due dates for each task with our intuitive drag-and-drop interface."
              },
              {
                title: "Cross-Device Sync",
                description: "Access your tasks from anywhere, on any device.",
                icon: "🔄",
                details: "All your tasks are synced in real-time across all your devices with our secure cloud technology."
              },
              {
                title: "Team Collaboration",
                description: "Share tasks and collaborate with your team in real-time.",
                icon: "👥",
                details: "Assign tasks to team members, track progress, and communicate directly within each task."
              },
              {
                title: "Productivity Insights",
                description: "Track your progress and identify productivity patterns.",
                icon: "📈",
                details: "Detailed analytics show your productivity trends and help you optimize your workflow."
              },
              {
                title: "Customizable Views",
                description: "Switch between list, calendar, and board views.",
                icon: "🎨",
                details: "Choose how you want to view your tasks - whether it's a simple list, calendar, or Kanban board."
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 hover:shadow-xl transition-shadow"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mb-3">
                  {feature.description}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {feature.details}
                </p>
              </div>
            ))}
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Ready to Transform Your Productivity?</h2>
              <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
                Join thousands of users who have transformed their productivity with TodoApp
              </p>
              <div className="flex flex-col sm:flex-row justify-center gap-4">
                <Link
                  href="/signup"
                  className="px-8 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:bg-indigo-700 transition-all"
                >
                  Start Free Trial
                </Link>
                <Link
                  href="/demo"
                  className="px-8 py-4 bg-white dark:bg-gray-700 text-gray-800 dark:text-white font-semibold rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 transition-all"
                >
                  Watch Demo
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="py-12 bg-gray-900 text-gray-400 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="text-2xl font-bold text-white mb-4">TodoApp</div>
          <p className="mb-6">© 2026 TodoApp. All rights reserved.</p>
          <div className="flex justify-center space-x-6">
            <Link href="/privacy" className="hover:text-white transition-colors">
              Privacy Policy
            </Link>
            <Link href="/terms" className="hover:text-white transition-colors">
              Terms of Service
            </Link>
            <Link href="/contact" className="hover:text-white transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}