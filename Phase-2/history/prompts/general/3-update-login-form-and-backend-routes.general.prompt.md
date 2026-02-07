---
id: 3
title: "Update Login Form and Backend Routes"
stage: "general"
date: "2026-02-02"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "Update login form and backend routes for manual fetch"
labels: ["auth", "fetch", "login", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/components/auth/LoginForm.tsx"
  - "backend/src/auth/router.py"
tests: []
---

# Update Login Form and Backend Routes

## Prompt Text
In frontend/components/auth/LoginForm.tsx, please rewrite the handleSubmit function to look exactly like this. Do not use any external hooks for a second, just pure logic:

JavaScript
const handleSubmit = async (e) => {
  e.preventDefault();
  console.log("SENDING DATA...", email, password); // Console mein check karein ye aata hai ya nahi
const response = await fetch('http://localhost:8000/api/auth/sign-in/email', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: email.trim(), password: password }) });

const result = await response.json(); if (response.ok && result.token) { localStorage.setItem('token', result.token); window.location.href = '/dashboard'; // Direct redirect } else { alert("Login Failed: " + (result.detail || "Unknown error")); } };


**Also, in the Backend `router.py`**:
Make sure the `/sign-in/email` route is using `body: dict = Body(...)` or a Pydantic model to catch this email and password correctly.

## Response Text
Updated the LoginForm component to use direct manual fetch approach and updated the backend routes to use Pydantic models:

1. Updated frontend/components/auth/LoginForm.tsx to use manual fetch with direct JSON body
2. Updated backend/src/auth/router.py to use LoginRequest Pydantic model for /sign-in/email endpoint
3. Updated /sign-up/email endpoint to use SignUpRequest Pydantic model
4. Changed redirect destination from '/dashboard' to '/tasks' to match existing app structure

## Outcome
Login form now uses direct manual fetch with proper JSON body, and backend routes properly handle requests using Pydantic models.

## Evaluation
- Login form sends proper JSON body with email and password
- Backend routes accept structured data via Pydantic models
- Proper error handling and response format maintained
- Token storage works correctly after successful login