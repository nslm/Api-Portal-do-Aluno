from fastapi import FastAPI
import re
import werkzeug
from pydantic import BaseModel
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser
from selenium import webdriver
from uuid import uuid4
import time
from bs4 import BeautifulSoup as bf


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


@app.post('/provas')
async def notas(login:login):

    driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver'
    url = 'https://portalence.ibge.gov.br/gcad-aluno/'

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
    driver.get(url)

    login = driver.find_element_by_xpath("//input[@id='login-form:matricula-aluno']").send_keys(login.matricula)
    password = driver.find_element_by_xpath("//input[@name='login-form:j_idt22']").send_keys(login.senha)
    submit = driver.find_element_by_xpath("//input[@name='login-form:j_idt24']").click()
    provas = driver.find_element_by_xpath("//body/div[contains(@class,'defTudo tudo')]/div[contains(@class,'defContainer row well bgbranco')]/div[contains(@class,'bgbranco')]/form[@id='j_idt46']/div[contains(@class,'dropdown clearfix')]/ul[contains(@class,'dropdown-menu')]/li[2]/a[1]").click()
    notas_das_provas = driver.find_element_by_xpath("//a[contains(text(),'Notas das Provas')]").click()

    soup=bf(driver.page_source)
    datalist = [] #empty list
    x = 0 #counter

    for i in soup.find_all(lambda tag: tag.name == 'tr'):
    datalist.append(i)

    time.sleep(5)

    driver.quit()

    return datalist
