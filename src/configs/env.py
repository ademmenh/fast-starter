import os
from src.types.env import enEnv

pyENV = os.getenv("pyENV")
inProd = True if pyENV == enEnv.prod else False
inDev = True if pyENV == enEnv.dev else False
inTest = True if pyENV == enEnv.test else False
