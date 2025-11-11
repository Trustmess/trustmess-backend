from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth import router as auth_router
from src.routes.users import router as user_router
from src.routes.websocket import router as websocket_router

app = FastAPI(
    title='TrustMess API',
    description="Real-time messaging API with WebSocket support",
    version='0.4.0'
)

# ? CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# * Root route
# *****************************************************************************
@app.get("/")
async def read_root():
    return {
        "status": "Ok",
        "docs": "/docs",
        "version": "0.4.0"
        }
# *****************************************************************************

# * Include routers
# *****************************************************************************
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(websocket_router)
# *****************************************************************************


# ? Run the app with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
