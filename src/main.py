import uvicorn
from fastapi import FastAPI
from database.db import init_db
from db_config import settings
from routers.todos import router



app = FastAPI()
app.include_router(router=router)
    
if __name__ == '__main__':
    init_db(),
    uvicorn.run(
        "main:app", 
        reload=True,
        host=settings.HOST,
        port=settings.PORT
    )