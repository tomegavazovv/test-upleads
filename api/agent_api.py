from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middleware.cors_middleware import add_cors_headers
from api.routers.agent_router import router

app = FastAPI(title="Agent API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://upleads-prod.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add CORS middleware handler
app.middleware("http")(add_cors_headers)

# Include routers
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=30) 