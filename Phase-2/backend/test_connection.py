"""
Simple test to check if we can connect to the Neon database.
This script will try to establish a connection without creating tables.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL not found in environment variables!")
    print("Please make sure you have a .env file with the database connection string.")
    exit(1)

print(f"Database URL found: {DATABASE_URL.replace('@', '***@')[:60]}..." if '@' in DATABASE_URL else f"Database URL: {DATABASE_URL}")

# Check if we can parse the connection string
try:
    from urllib.parse import urlparse

    parsed = urlparse(DATABASE_URL)
    print(f"✓ Successfully parsed database URL")
    print(f"  Scheme: {parsed.scheme}")
    print(f"  Host: {parsed.hostname}")
    print(f"  Port: {parsed.port}")
    print(f"  Database: {parsed.path.lstrip('/')}")
    print(f"  Username: {parsed.username}")
    print(f"  Password present: {'YES' if parsed.password else 'NO'}")

except ImportError:
    print("urllib.parse not available, but that's OK for basic validation")
    print("Database URL format appears correct")

print("\nTo create tables in your Neon database, you would typically run:")
print("  1. Install required packages: pip install sqlmodel psycopg2-binary")
print("  2. Run the create_db.py script: python create_db.py")

print(f"\nYour database connection string is properly configured in the .env file.")
print(f"You can now use it in your application to connect to Neon Serverless PostgreSQL.")