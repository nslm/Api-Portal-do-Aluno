from fastapi import FastAPI
import re
import werkzeug
from pydantic import BaseModel
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser
from uuid import uuid4

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
    def new_token():
        return uuid4()

    br = RoboBrowser()
    br.open(url)
    form = br.get_form()
    form['login-form:matricula-aluno'] = login.matricula
    form['login-form:j_idt22'] = login.senha
    br.submit_form(form)
    page = str(br.parsed())
    isOn = False
    name = ''
    token = ''
    if '<!-- L O G I N  &amp;  N O M E-->' in page:
        isOn = True
        start = 'Nome: '
        end = ' '
        name = re.search('%s(.*)%s' % (start, end), page).group(1)
        token = new_token()
    return {'Status':isOn, 'name':name, 'token':token}




