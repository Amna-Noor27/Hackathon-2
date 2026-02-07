import { NextRequest, NextResponse } from 'next/server';

// Protect routes that require authentication
export function middleware(request: NextRequest) {
  // Define protected routes
  const protectedPaths = ['/tasks'];
  const currentPath = request.nextUrl.pathname;

  // Check if the current path is protected
  const isProtected = protectedPaths.some(path =>
    currentPath === path || currentPath.startsWith(path + '/')
  );

  // For protected routes, we'll rely on client-side auth check in the component
  // since localStorage is not available in middleware
  // We'll still check for the token in cookies if available
  if (isProtected) {
    // In a real-world scenario, you'd typically have the token in cookies
    // For now, we'll allow the request and handle auth on the client side
    // The ProtectedRoute component will handle the actual redirect

    // For now, just continue - the client-side ProtectedRoute component will handle authentication
    return NextResponse.next();
  }

  // Allow the request to continue
  return NextResponse.next();
}

// Apply middleware to specific paths
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};