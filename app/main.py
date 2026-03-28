from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="eCommerce Inventory Automation System",
    version="1.0.0",
    description="Analyze inventory, generate reorder recommendations, and export operational reports.",
)

app.include_router(router)
