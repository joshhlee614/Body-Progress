from fastapi import FastAPI
import asyncpg
import os
from dotenv import load_dotenv
from app.api.users.router import router as users_router

load_dotenv()

app = FastAPI()
db_pool = None

@app.on_event('startup')
async def startup():
    global db_pool
    db_pool = await asyncpg.create_pool(os.getenv('DATABASE_URL'))

@app.on_event('shutdown')
async def shutdown():
    await db_pool.close()

# include routers
app.include_router(users_router)

@app.get('/')
def read_root():
    # return a simple message for health check
    return {'message': 'backend is running'}

@app.get('/health')
def health_check():
    return {'status': 'ok'}
