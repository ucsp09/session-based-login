from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.user_api import user_api_router
from api.login_api import login_api_router
from core.bootstrap import startup_event_handler, shutdown_event_handler

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.root_path = "/api/v1"
app.include_router(user_api_router)
app.include_router(login_api_router)
app.add_event_handler("startup", startup_event_handler)
app.add_event_handler("shutdown", shutdown_event_handler)