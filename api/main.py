import logging
import json
from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .dependencies import verify_credentials
from .routers import sensor_readings


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(dependencies=[Depends(verify_credentials)])
app.include_router(sensor_readings.app)


# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error for {request.method} {request.url}")
    logger.error(f"Validation errors: {exc.errors()}")

    # Try to get the raw body for debugging
    try:
        body = await request.body()
        logger.error(f"Raw request body: {body.decode()}")

        # Try to parse as JSON to see the structure
        if body:
            try:
                json_body = json.loads(body.decode())
                logger.error(f"Parsed JSON structure: {json.dumps(json_body, indent=2)}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {e}")
    except Exception as e:
        logger.error(f"Could not read request body: {e}")

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Validation failed - check the logs for details"
        }
    )


# debug
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Content-Type: {request.headers.get('content-type')}")

    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")

    return response
