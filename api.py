from fastapi import FastAPI
import re
import werkzeug
from pydantic import BaseModel
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
async def Login(login:login):

    url = 'https://portalence.ibge.gov.br/gcad-aluno/login.jsf'
    br = RoboBrowser()
    br.open(url)

    form = br.get_form()
    form['login-form:matricula-aluno'] = login.matricula
    form['login-form:j_idt22'] = login.senha
    br.submit_form(form)
    page = str(br.parsed())
    return {'detail':page} #{'pagina': page}
    #if 'Login e senha de usuário não conferem no sistema.' in page:
        #return False
    #return True




