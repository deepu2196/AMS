from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Apartment Management System")

@app.get("/")
def read_root():
    return {"msg": "Apartment Management System"}