from fastapi import FastAPI
from routers import post
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware

# dbを生成している
models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
    )

app.include_router(post.router)

@app.get("/")
def index():
    return {"message": "Hello World"}

if __name__ == '__main__':
    app.run()