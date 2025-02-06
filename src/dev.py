import os
import uvicorn
import src.utils.env
from src.types.env import enEnv

os.environ['pyENV'] = enEnv.dev

if __name__ == '__main__':
    uvicorn.run("src.app:app", port=8000, reload=True)
