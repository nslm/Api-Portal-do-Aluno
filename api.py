import re
import time
import werkzeug
import sqlite3

werkzeug.cached_property = werkzeug.utils.cached_property

from uuid import uuid4
from fastapi import FastAPI
from selenium import webdriver
from pydantic import BaseModel
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup as bf


from notas import Notas
from login import Login



class login(BaseModel):
    matricula: str 
    senha: str




app = FastAPI()



@app.get("/")
async def root():
    return 'Api simples para scrap do portal do aluno da ence'



@app.post("/login")
async def login(login:login):
    return Login(login.matricula, login.senha)



@app.post('/notas')
async def notas(token):
    return Notas(token)



@app.post('/inscritas')
async def inscritas(token):
    #return Inscritas(token)
    pass
