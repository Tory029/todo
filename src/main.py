import uvicorn
from fastapi import FastAPI
from db import init_db
from db_config import settings

from routers.todo import router
from routers.todo_list import router2



app = FastAPI()
app.include_router(router)
app.include_router(router2)
    
if __name__ == '__main__':
    init_db()
    uvicorn.run(
        "main:app", 
        reload=True,
        host=str(settings.HOST),
        port=int(settings.PORT),
    )
