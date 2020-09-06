from fastapi import FastAPI
import re
import werkzeug
from pydantic import BaseModel
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser

url = 'https://portalence.ibge.gov.br/gcad-aluno/'

class login(BaseModel):
    matricula: str 
    senha: str


app = FastAPI()


@app.get("/")
async def root():
    return 'Api simples para scrap do portal do aluno da ence'

@app.post("/")
async def login(login:login):
    br = RoboBrowser()
    br.open(url)
    form = br.get_form()
    form['login-form:matricula-aluno'] = login.matricula
    form['login-form:j_idt22'] = login.senha
    br.submit_form(form)
    page = str(br.parsed())


@app.post("/login")
async def Login(login:login):

    br = RoboBrowser()
    br.open(url)

    form = br.get_form()
    form['login-form:matricula-aluno'] = login.matricula
    form['login-form:j_idt22'] = login.senha
    br.submit_form(form)
    page = str(br.parsed())
    return page 

@app.get("/provas")
async def provas():
    


