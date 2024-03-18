from fastapi import APIRouter

from .v1.endpoints import api_task_crud

api_router = APIRouter()

routers = [
    (api_task_crud.router, "/v1", ["api_task_crud"]),
]

for router, prefix, tags in routers:
    api_router.include_router(router, prefix=prefix, tags=tags)  # type: ignore
