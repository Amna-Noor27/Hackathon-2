---
id: 2
title: "Switch from authClient to localStorage token in useTasks hook"
stage: "general"
date: "2026-02-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "switch from authClient.getSession() to localStorage token in useTasks hook"
labels: ["authentication", "frontend", "bug-fix", "security"]
spec: null
ticket: null
pr: null
adr: null
---

## Files Modified
 - D:/Hackathon-II/Phase-2/frontend/hooks/useTasks.ts

## Prompt Text
I am getting a 'Failed to fetch' error on authClient.getSession(). Since we are using manual login, we should not rely on the client session here.

Please update hooks/useTasks.ts:

Remove or Comment out the authClient.getSession() call.

Get Token Directly: Use const token = localStorage.getItem('token'); at the start of the fetchTasks function.

Check Token: If no token is found, redirect to login or show an error.

Fetch Logic: Ensure the fetch call uses this token in the headers: 'Authorization': 'Bearer ' + token

Goal: Stop the authClient from crashing the task fetching logic.

## Response Text
Updated the useTasks hook to remove dependency on authClient.getSession() and instead use localStorage token directly for authentication. Modified all functions (fetchTasks, createTask, updateTask, deleteTask) to get the token from localStorage.getItem('token') and redirect to login if no token is found. Removed the authClient import as it's no longer needed in this file.

## Outcome
Successfully removed authClient.getSession() calls from the useTasks hook and replaced them with direct localStorage token access. The task fetching logic no longer crashes due to authClient failures, and authentication now works reliably using tokens stored in localStorage.

## Evaluation
- Removed authClient.getSession() calls from all functions in useTasks hook
- Added localStorage token retrieval with proper error handling
- Implemented redirect to login when no token is found
- Maintained proper authorization headers for API calls
- Removed unused authClient import
- Fixed the 'Failed to fetch' error for task operations