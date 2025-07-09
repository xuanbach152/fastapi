from fastapi import  FastAPI

from app.controllers.user_controller import router as user_router
from app.controllers.auth_controller import router as auth_router



from app.db.init_db import init_database

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Hello World"}
init_database()
