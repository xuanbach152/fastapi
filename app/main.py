from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from app.controllers.user_controller import router as user_router
from app.controllers.auth_controller import router as auth_router
from app.controllers.product_controller import router as product_router


from app.db.init_db import init_database

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(product_router)

app.mount("/image/product", StaticFiles(directory="app/image/product"), name="product_images")  



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Hello World"}
init_database()
