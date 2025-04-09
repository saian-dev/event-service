from contextlib import asynccontextmanager

from app.api.routers import router_v1
from app.core.database import sessionmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, docs_url="/api/docs")
app.include_router(router_v1, prefix="/api")
