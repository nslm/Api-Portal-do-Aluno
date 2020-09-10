
import re

from selenium import webdriver
from bs4 import BeautifulSoup as bf


def Notas(matricula, senha):

    driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver'
    url = 'https://portalence.ibge.gov.br/gcad-aluno/'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
    driver.get(url)
    login = driver.find_element_by_xpath("//input[@id='login-form:matricula-aluno']").send_keys(matricula)
    password = driver.find_element_by_xpath("//input[@name='login-form:j_idt22']").send_keys(senha)
    submit = driver.find_element_by_xpath("//input[@name='login-form:j_idt24']").click()
    provas = driver.find_element_by_xpath("//body/div[contains(@class,'defTudo tudo')]/div[contains(@class,'defContainer row well bgbranco')]/div[contains(@class,'bgbranco')]/form[@id='j_idt46']/div[contains(@class,'dropdown clearfix')]/ul[contains(@class,'dropdown-menu')]/li[2]/a[1]").click()
    notas_das_provas = driver.find_element_by_xpath("//a[contains(text(),'Notas das Provas')]").click()
    datalist = []
    soup=bf(driver.page_source, 'html.parser')
    driver.quit()
    for materia in soup.find_all(lambda tag: tag.name == 'tr'):
        datalist.append(str(materia))
    print(datalist)
    return datalist[4]
    