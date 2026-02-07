import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6 max-w-7xl mx-auto">
        <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">TodoApp</div>
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

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900 dark:text-white mb-6">
            Organize Your Life with <span className="text-indigo-600 dark:text-indigo-400">TodoApp</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-10">
            The simplest way to manage your tasks, boost productivity, and achieve your goals.
            Get started today and transform the way you organize your life.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              href="/signup"
              className="px-8 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:bg-indigo-700 transition-all transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              Get Started - It&apos;s Free 😎
            </Link>
            <Link
              href="/login"
              className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-800 dark:text-white font-semibold rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all"
            >
              Log In to Your Account
            </Link>
          </div>
        </div>
      </section>

      {/* Preview Section */}
      <section className="py-16 bg-white dark:bg-gray-800 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">See How It Works</h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Experience our intuitive task management interface
            </p>
          </div>

          <div className="bg-gray-50 dark:bg-gray-700 rounded-2xl p-6 max-w-4xl mx-auto shadow-xl">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Sample Tasks</h3>
              <button className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300">
                + Add New
              </button>
            </div>

            <div className="space-y-4">
              {[1, 2, 3].map((item) => (
                <div
                  key={item}
                  className="flex items-center p-4 bg-white dark:bg-gray-600 rounded-lg shadow-sm border border-gray-200 dark:border-gray-500"
                >
                  <input
                    type="checkbox"
                    className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
                    aria-label="Task completion checkbox"
                  />
                  <span className={`ml-3 flex-1 text-gray-800 dark:text-gray-200 ${item === 2 ? 'line-through text-gray-500 dark:text-gray-400' : ''}`}>
                    {item === 1 && 'Complete the project proposal'}
                    {item === 2 && 'Review team feedback (completed)'}
                    {item === 3 && 'Prepare for tomorrow\'s meeting'}
                  </span>
                  <button className="text-gray-400 hover:text-red-500 dark:hover:text-red-400 ml-2">
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Powerful Features</h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Everything you need to stay organized and productive
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Smart Organization",
                description: "Intelligent categorization and tagging to keep your tasks organized.",
                icon: "📊"
              },
              {
                title: "Priority Management",
                description: "Set priorities and deadlines to focus on what matters most.",
                icon: "⚡"
              },
              {
                title: "Cross-Device Sync",
                description: "Access your tasks from anywhere, on any device.",
                icon: "🔄"
              },
              {
                title: "Team Collaboration",
                description: "Share tasks and collaborate with your team in real-time.",
                icon: "👥"
              },
              {
                title: "Productivity Insights",
                description: "Track your progress and identify productivity patterns.",
                icon: "📈"
              },
              {
                title: "Customizable Views",
                description: "Switch between list, calendar, and board views.",
                icon: "🎨"
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 hover:shadow-xl transition-shadow"
              >
                <div className="text-3xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-indigo-600 dark:bg-indigo-800">
        <div className="max-w-7xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h2>
          <p className="text-xl text-indigo-100 max-w-2xl mx-auto mb-8">
            Join thousands of users who have transformed their productivity with TodoApp
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              href="/signup"
              className="px-8 py-4 bg-white text-indigo-600 font-semibold rounded-lg shadow-lg hover:bg-gray-100 transition-all transform hover:-translate-y-0.5"
            >
              Create Free Account
            </Link>
            <Link
              href="/features"
              className="px-8 py-4 bg-transparent text-white font-semibold rounded-lg border border-white hover:bg-indigo-700 transition-all"
            >
              Explore Features
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-gray-900 text-gray-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
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
        </div>
      </footer>
    </div>
  );
}