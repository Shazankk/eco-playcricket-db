import sys
import os
from pathlib import Path

# Debug information
# print("Python path:\n", sys.path)
# print("Python version:\n", sys.version)
# print("Python executable:\n", sys.executable)
# print("Site packages:\n", Path(sys.__name__).parent / 'site-packages')

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from controllers.api_controller import router
    import uvicorn
except ImportError as e:
    print(f"Import error: {e}")
    print("\nInstalled packages:")
    os.system('pip list')
    sys.exit(1)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
