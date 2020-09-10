from fastapi import FastAPI
from pydantic import BaseModel

from notas import Notas
from login import Login


class login_form(BaseModel):
    matricula: str 
    senha: str





app = FastAPI()



@app.get("/")
async def root():
    return 'Api simples para scrap do portal do aluno da ence'



@app.post("/login")
async def login(login:login_form):
    return Login(login.matricula, login.senha)



@app.post('/notas')
async def notas(login:login_form):
    return Notas(login.matricula, login.senha)



@app.post('/inscritas')
async def inscritas(token):
    #return Inscritas(token)
    pass
