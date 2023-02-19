from fastapi import FastAPI
import uvicorn

def server_main():
    app = FastAPI()

    @app.get('/')
    async def hello():
        return "Hello, world!"
    
    uvicorn.run(app, host="0.0.0.0", port=1127)
