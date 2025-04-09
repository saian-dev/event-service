from contextlib import asynccontextmanager

import uvicorn
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
