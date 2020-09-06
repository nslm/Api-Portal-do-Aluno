from fastapi import FastAPI
import re
import werkzeug
from pydantic import BaseModel
from config import matricula
from config import senha
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser

app = FastAPI()


@app.get("/")
async def root():
    return 'minha primeira api'


class login(BaseModel):
    matricula: str 
    senha: str


@app.post("/login")
async def isLogin(login:login):

    url = 'https://portalence.ibge.gov.br/gcad-aluno/login.jsf'
    br = RoboBrowser()
    br.open(url)

    form = br.get_form()
    form['login-form:matricula-aluno'] = matricula
    form['login-form:j_idt22'] = senha
    br.submit_form(form)
    page = str(br.parsed())
    return {'detail':page} #{'pagina': page}
    #if 'Login e senha de usuário não conferem no sistema.' in page:
        #return False
    #return True




