import reflex as rx
from dotenv import load_dotenv
import os

load_dotenv()
BACKEND_PORT = os.getenv("BACKEND_PORT", 8001)
FRONTEND_PORT = os.getenv("FRONTEND_PORT", 3000)

config = rx.Config(
    app_name="chatapp",
    backend_port=BACKEND_PORT,
    frontend_port=FRONTEND_PORT,
)