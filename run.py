"""
Run this file to start both servers at once:
    python run.py
"""
import subprocess, sys, os, time, webbrowser

ROOT    = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.join(ROOT, "backend")

print("Starting FastAPI backend on http://localhost:8000 ...")
api = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
    cwd=BACKEND
)

time.sleep(2)

print("Starting Streamlit frontend on http://localhost:8501 ...")
ui = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app.py"],
    cwd=ROOT
)

time.sleep(3)
webbrowser.open("http://localhost:8501")

print("\n✅ Both servers running.")
print("   Streamlit  → http://localhost:8501")
print("   API docs   → http://localhost:8000/docs")
print("\nPress Ctrl+C to stop both.\n")

try:
    api.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    api.terminate()
    ui.terminate()
