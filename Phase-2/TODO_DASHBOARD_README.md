# Todo Dashboard

A modern, responsive todo dashboard built with Next.js App Router, TypeScript, and Tailwind CSS.

## Features

- **Task Management**: Create, read, update, and delete tasks
- **Task Status**: Mark tasks as complete/incomplete
- **Search/Filter**: Find tasks by title or description
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Form Validation**: Client-side validation for task creation
- **Loading States**: Visual feedback during API operations
- **Error Handling**: Graceful error handling with retry functionality
- **Edit Functionality**: Inline editing of task details
- **Modern UI**: Clean, intuitive interface with Tailwind CSS

## Components

### Dashboard Page (`app/dashboard/page.tsx`)
- Main dashboard interface
- Task list display
- Search functionality
- Loading and error states

### Task Item (`app/dashboard/components/TaskItem.tsx`)
- Individual task display
- Completion checkbox
- Edit/delete functionality
- Responsive layout

### Task Form (`app/dashboard/components/TaskForm.tsx`)
- Task creation form
- Validation
- Submission handling

### API Utilities (`app/dashboard/lib/api.ts`)
- Functions to interact with the backend API
- Authentication handling
- CRUD operations for tasks

### Context Provider (`app/dashboard/context/DashboardContext.tsx`)
- State management for the dashboard
- Reducer-based state updates
- Business logic encapsulation

## API Integration

The dashboard connects to a FastAPI backend with the following endpoints:
- `GET /tasks` - Retrieve all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Base URL for the backend API (defaults to `http://localhost:8000/api`)

## Responsive Design

The dashboard uses Tailwind CSS utility classes to provide a responsive experience:
- Mobile-first approach
- Flexbox and Grid layouts
- Responsive breakpoints for different screen sizes
- Touch-friendly controls

## Error Handling

- Global error boundary for unexpected errors
- Component-level error handling
- Retry functionality for failed API calls
- User-friendly error messages

## Accessibility

- Semantic HTML structure
- Proper ARIA attributes
- Keyboard navigation support
- Sufficient color contrast
- Focus management

## Getting Started

1. Set up your Next.js project with Tailwind CSS
2. Install required dependencies
3. Configure your backend API endpoint
4. Run the development server