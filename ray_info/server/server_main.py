from fastapi import FastAPI
import uvicorn

from ray_info.db import Info


def server_main():
    app = FastAPI()

    @app.get("/")
    async def hello():
        return "Hello, world!"

    @app.get("/info/list")
    async def info_list(page: int = 1, per_page: int = 20):
        query = Info.select().order_by(Info.updated.desc())
        total = query.count()
        info_list = query.paginate(page, per_page)
        return {
            "total": total,
            "info_list": [info.__dict__["__data__"] for info in info_list],
        }

    uvicorn.run(app, host="0.0.0.0", port=1127)
