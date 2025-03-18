from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.api_controller import router
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os


app = FastAPI(title="Colchester Cavs API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router, prefix="/api/v1")

def run_pipeline_job():
    pipeline_script = os.path.join(os.path.dirname(__file__), "run_pipeline.py")
    cmd = [os.path.join(os.path.dirname(__file__), ".venv", "bin", "python"), pipeline_script]
    subprocess.run(cmd)
    print("Pipeline job ran successfully")

scheduler = BackgroundScheduler(daemon = True)
scheduler.add_job(run_pipeline_job, "interval", hours=24)
scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
