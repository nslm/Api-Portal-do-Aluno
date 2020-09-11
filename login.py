import re
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

from robobrowser import RoboBrowser



def Login(matricula,senha):              

    url = 'https://portalence.ibge.gov.br/gcad-aluno/'

    br = RoboBrowser()
    br.open(url)
    form = br.get_form()
    form['login-form:matricula-aluno'] = matricula
    form['login-form:j_idt22'] = senha
    br.submit_form(form)
    page = str(br.parsed())
    loged = False
    name = ''
    if '<!-- L O G I N  &amp;  N O M E-->' in page:
        loged = True
        start = 'Nome: '
        end = ' '
        name = re.search('%s(.*)%s' % (start, end), page).group(1)
        name = name.lower()


    return { 'status':loged, 'name':name}