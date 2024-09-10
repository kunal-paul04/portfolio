from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
'''import database connection for mongoDB'''
from lib.mongo_lib import database_connection
conn = database_connection()

app = FastAPI()





