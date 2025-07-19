import uvicorn
from prompt_bot import app_instance

if __name__ == "__main__":
    uvicorn.run(app_instance, host="0.0.0.0", port=8000)
