from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    # return a simple message for health check
    return {'message': 'backend is running'}
