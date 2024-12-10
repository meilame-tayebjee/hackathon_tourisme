import os
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel
from typing import Annotated, List
import uvicorn
import sys

sys.path.append('../')
# Import the existing launch function
from src.main import launch

# Create a Pydantic model for input validation
class RouteRequest(BaseModel):
    api_key: str
    start_lat: float
    start_lon: float
    radius: float = 20
    top_k: int = 5


# Initialize FastAPI app with explicit OpenAPI configuration
app = FastAPI(
    title="Route Optimizer API",
    description="API for optimizing routes based on location data",
    version="0.1.0",
    root_path="/proxy/8000"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins if necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Welcome"])
def show_welcome_page():
    """
    Show welcome page with model name and version.
    """

    return {
        "Message": "Routing de tourisme accessible",
        "Model_version": "0.0.1"}


@app.get("/optimize-route")
async def optimize_route(api_key, start_lat, start_lon, radius, top_k):
    """
    Endpoint to optimize a route based on input parameters
    
    - **api_key**: Google Maps API key
    - **start_lat**: Starting latitude
    - **start_lon**: Starting longitude
    - **radius**: Search radius (default 20)
    - **top_k**: Number of top locations to retrieve (default 5)
    """
    try:
        final_route = launch(
            str(api_key), 
            float(start_lat), 
            float(start_lon), 
            int(radius), 
            int(top_k)
        )
        return {"route": final_route}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: Add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Main block for running the server directly
if __name__ == "__main__":
    uvicorn.run(
        "api.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )