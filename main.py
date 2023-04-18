import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from user.api import user_router
from user.api_login import login_router

# create instance of the app
app = FastAPI(title="My API", version="1.0.0")

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
