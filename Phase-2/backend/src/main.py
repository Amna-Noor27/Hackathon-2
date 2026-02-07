from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import tasks
from src.auth.router import router as auth_router
from src.database import engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from src.middleware.error_handler import add_error_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create or update database tables on startup
    # This will create tables if they don't exist or update them if needed
    from sqlmodel import SQLModel
    # Create tables if they don't exist (don't drop existing data)
    # In production, use proper migrations
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title="Todo Task Management API",
    description="API for managing user tasks",
    version="1.0.0",
    lifespan=lifespan
)

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type", "X-Requested-With"],
    # Expose headers that frontend needs to access
    expose_headers=["Authorization", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
)

# Add error handlers
add_error_handlers(app)

# --- INCLUDE ROUTES ---

app.include_router(auth_router, prefix="/api/auth", tags=["authentication"]) 
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": " ✍️ Todo Backend API is running!"}

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"REQUEST HEADERS: {dict(request.headers)}")
    response = await call_next(request)
    return response


@app.get("/health")
def health_check():
    return {"status": "healthy"}
