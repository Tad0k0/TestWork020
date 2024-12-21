from fastapi import FastAPI, Depends
import uvicorn

from transaction.router import router

from common.security import check_api_key
from config import settings

ACCESS_CHECK = [Depends(check_api_key)]

app = FastAPI(
    title="TestWork020"
)

app.include_router(router, dependencies=ACCESS_CHECK)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
