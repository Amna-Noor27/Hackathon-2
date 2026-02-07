# 🚀 Full-Stack Task Management System (Phase 1 & 2)

Welcome to the **Hackathon-II** Task Management System. This project is a comprehensive full-stack application built with high-performance frameworks, focusing on security, scalability, and a seamless user experience.

---

## 📂 Project Structure

The project is organized into two distinct phases to demonstrate progress and architectural growth:

* **📁 Phase-1:** Core Todo functionality and basic API setup.
* **📁 Phase-2:** Advanced features including Authentication (Better-Auth), Database persistence (Neon DB), and production-grade deployment.

---

## ✨ Key Features & Technical Stack

### 🛠 Backend (FastAPI)
* **Asynchronous Processing:** Built with Python's FastAPI for high-concurrency.
* **Database:** PostgreSQL hosted on **Neon DB** (Serverless).
* **ORM:** **SQLModel** for seamless integration between Python classes and SQL tables.
* **Security:** * **Better-Auth** integration for secure session management.
    * JWT-based authentication.
    * CORS protection for cross-origin security.
* **Deployment:** Hosted on **Hugging Face Spaces**.

### 💻 Frontend (Next.js)
* **Framework:** Next.js 14/15 (App Router).
* **Styling:** **Tailwind CSS** for a modern, responsive interface.
* **State Management:** Client-side handling for real-time task updates.
* **Deployment:** Hosted on **Vercel**.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- Neon DB Account (PostgreSQL)

### 2. Backend Setup
```bash
cd Phase-2/backend
pip install -r requirements.txt

# Create a .env file with your DATABASE_URL and SECRET_KEY
uvicorn src.main:app --reload
```
3. Frontend SetupBashcd Phase-2/frontend
npm install
npm run dev
🔧 Advanced Features ImplementedMulti-Phase Architecture: Clear separation of development stages for better maintainability.Identity Isolation: Users can only access, edit, or delete their own tasks.Persistent Sessions: Modern authentication flow that keeps users logged in securely.Database Migrations: Structured schema handling for evolving data requirements.Deployment Pipelines: Configured for CI/CD environments on Vercel and Hugging Face.

🔗 Live Demo & RepositoryResourceLinkFrontend URL[https://frontend-one-vert-63.vercel.app/] GitHub Repo[https://github.com/Amna-Noor27/Hackathon-2]

👩‍💻 Author
Amna Noor Full-Stack Developer Enthusiast [[LinkedIn Profile](https://www.linkedin.com/in/amnanoor27/)] | [[GitHub Profile](https://github.com/Amna-Noor27/)]
