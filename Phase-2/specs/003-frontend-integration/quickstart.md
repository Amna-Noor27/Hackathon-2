# Quickstart Guide: Frontend Integration

## Overview
This guide provides instructions for setting up and running the frontend application for the Todo Full-Stack Web Application. The frontend is built with Next.js using App Router and integrates with the backend APIs and authentication system.

## Prerequisites
- Node.js 18+
- npm or yarn package manager
- Backend API from Spec-1 (Todo Backend Tasks) running
- Authentication system from Spec-2 (Auth Security) configured
- Better Auth configured with shared secret

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Navigate to frontend directory
```bash
cd frontend
```

### 3. Install dependencies
```bash
npm install
# or
yarn install
```

### 4. Environment Configuration
Create a `.env.local` file in the frontend directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-shared-secret-key-here-replace-with-a-real-secret
NEXT_PUBLIC_JWT_SECRET=your-shared-secret-key-here-replace-with-a-real-secret
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8080
```

### 5. Next.js Configuration
Make sure your `next.config.js` includes the necessary settings:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true, // Enables App Router
  },
  images: {
    domains: ['localhost', 'your-backend-domain.com'],
  },
  async redirects() {
    return [
      // Redirect from root to tasks page if authenticated
      {
        source: '/',
        destination: '/tasks',
        permanent: false,
        has: [
          {
            type: 'cookie',
            key: 'access_token',
          },
        ],
      },
      // Redirect from root to login if not authenticated
      {
        source: '/',
        destination: '/login',
        permanent: false,
        missing: [
          {
            type: 'cookie',
            key: 'access_token',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig
```

### 6. Tailwind CSS Configuration
Ensure your `tailwind.config.js` is set up for responsive design:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      screens: {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      }
    },
  },
  plugins: [],
}
```

### 7. Run the Application
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`.

## Frontend Architecture

### Next.js App Router Structure
- `app/layout.tsx` - Root layout with global styles and providers
- `app/page.tsx` - Home page (redirects based on auth status)
- `app/login/page.tsx` - Login page
- `app/register/page.tsx` - Registration page
- `app/tasks/page.tsx` - Tasks list page
- `app/tasks/[id]/page.tsx` - Individual task page
- `app/tasks/new/page.tsx` - Create task page

### Component Structure
- `components/ui/` - Base UI components (buttons, inputs, etc.)
- `components/auth/` - Authentication-related components
- `components/tasks/` - Task-specific components
- `components/layout/` - Layout components (header, sidebar, footer)

### Hooks
- `hooks/useAuth.ts` - Authentication state management
- `hooks/useTasks.ts` - Task data management
- `hooks/useLocalStorage.ts` - Local storage utilities

### API Integration
- `lib/api.ts` - API client with JWT handling
- `lib/auth.ts` - Authentication utilities
- `middleware.ts` - Authentication middleware

## API Integration

### Authentication Flow
1. User visits `/login` or `/register` page
2. Better Auth handles authentication
3. JWT token is received and stored in browser
4. All subsequent API requests include the token in Authorization header

### Task Management Flow
1. User accesses `/tasks` page (protected route)
2. Application fetches user's tasks from `/api/tasks`
3. User can create, update, delete tasks via API endpoints
4. All operations are scoped to the authenticated user

## Testing
Run the tests using Jest and React Testing Library:
```bash
# Unit tests
npm run test
# or
yarn test

# E2E tests (if Cypress is configured)
npm run e2e
# or
yarn e2e
```

## Responsive Design
The application uses Tailwind CSS utility classes to ensure proper responsiveness:
- Mobile-first approach with breakpoints at 640px, 768px, 1024px
- Flexible grid layouts that adapt to screen size
- Touch-friendly UI elements for mobile devices
- Properly sized tap targets for mobile interaction

## State Management
- Authentication state managed through React Context API
- Task data fetched server-side for initial loads
- Client-side state managed with React hooks
- Loading, error, and empty states handled consistently across components

## Security Considerations
- JWT tokens stored securely in browser
- Protected routes implemented with authentication checks
- All API requests include proper authentication headers
- Input validation performed on both frontend and backend