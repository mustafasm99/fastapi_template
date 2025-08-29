from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.core.settings import settings
from app.endpoints.main import router as api_router
from fastapi.middleware.cors import CORSMiddleware


def custom_generate_unique_id(router:APIRoute):
     return f"{router.tags[0]}-{router.name}"


app = FastAPI(
     title=settings.PROJECT_NAME,
     openapi_url=f"/api/{settings.PROJECT_NAME}/{settings.API_VERSION}/openapi.json",
     generate_unique_id_function=custom_generate_unique_id,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)