from dotenv import load_dotenv
from src.configs.env import *

def loadENV():
    if inProd: load_dotenv()
    elif inTest: load_dotenv('env.test')
    elif inDev: load_dotenv('.env.dev')

loadENV()