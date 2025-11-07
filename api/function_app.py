import azure.functions as func
from fastapi.middleware.cors import CORSMiddleware
from api.main import app as fastapi_app
from mangum import Mangum

# Allow CORS if needed
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an Azure Function handler
handler = Mangum(fastapi_app)

app = func.AsgiFunctionApp(app=fastapi_app)
