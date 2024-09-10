from fastapi import FastAPI
from routes.routes import route
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(route)
