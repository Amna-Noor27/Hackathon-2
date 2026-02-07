export default function DemoPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">TodoApp Demo</h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-12">
          Experience the power of TodoApp with our interactive demo
        </p>

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-12">
          <div className="aspect-video bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center mb-6">
            <div className="text-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-gray-500 mt-4">Demo video player would appear here</p>
            </div>
          </div>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">Take a Tour</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            Watch our 3-minute demo to see how TodoApp can transform your productivity workflow.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[
            { title: "Task Management", desc: "Create, organize, and prioritize your tasks" },
            { title: "Collaboration", desc: "Work together with your team in real-time" },
            { title: "Analytics", desc: "Track your productivity and insights" }
          ].map((feature, index) => (
            <div key={index} className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-300">{feature.desc}</p>
            </div>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <a
            href="/signup"
            className="px-8 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:bg-indigo-700 transition-all"
          >
            Start Free Trial
          </a>
          <a
            href="/"
            className="px-8 py-4 bg-white dark:bg-gray-700 text-gray-800 dark:text-white font-semibold rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 transition-all"
          >
            Back to Home
          </a>
        </div>
      </div>
    </div>
  );
}