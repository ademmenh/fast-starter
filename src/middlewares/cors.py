from fastapi.middleware.cors import CORSMiddleware
from src.configs.env import *
from src.configs.cors import *

def configCORS (app):
    if inProd:
        app.add_middleware(
        CORSMiddleware,
        allow_origins = prodOrigins,
        allow_credentials = prodAllowedCredentials,
        allow_methods = prodMethods,
        allow_headers = prodHeaders,
        )
    elif inDev:
        app.add_middleware(
        CORSMiddleware,
        allow_origins = devOrigins,
        allow_credentials = devAllowedCredentials,
        allow_methods = devMethods,
        allow_headers = devHeaders,
        )
