export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Privacy Policy</h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Last updated: January 24, 2026
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
          <div className="prose prose-gray dark:prose-invert max-w-none">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Information We Collect</h2>
            <p className="mb-4">
              We collect information you provide directly to us, such as when you create an account, use our Services, or communicate with us.
            </p>

            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 mt-8">How We Use Information</h2>
            <p className="mb-4">
              We use information about you to provide, maintain, and improve our Services, and to communicate with you.
            </p>

            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 mt-8">Data Security</h2>
            <p className="mb-4">
              We implement appropriate technical and organizational measures to protect your personal data against unauthorized access, alteration, disclosure, or destruction.
            </p>

            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 mt-8">Contact Us</h2>
            <p className="mb-4">
              If you have questions about this Privacy Policy, please contact us at privacy@todoapp.com.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}