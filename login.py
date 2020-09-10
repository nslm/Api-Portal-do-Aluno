import re
import werkzeug
import sqlite3

werkzeug.cached_property = werkzeug.utils.cached_property

from uuid import uuid4
from robobrowser import RoboBrowser



def Login(matricula,senha):

    def new_token():
        conn = sqlite3.connect("Users.db") 
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM users;
        """)
        while True:
            token = uuid4()
            tokens = list()
            for linha in cursor.fetchall():
                tokens.append(token)
            if token not in tokens:
                return token
                

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
    token = ''
    if '<!-- L O G I N  &amp;  N O M E-->' in page:
        conn = sqlite3.connect("Users.db") 
        cursor = conn.cursor()

        loged = True
        start = 'Nome: '
        end = ' '
        name = re.search('%s(.*)%s' % (start, end), page).group(1)
        token = new_token()
        existUser = False

        for linha in cursor.fetchall():
            if matricula in linha:
                params = (matricula, senha, token)
                cursor.execute("""
                UPDATE users
                SET senha = ?, token = ?
                WHERE matricula= ?
                """, (matricula, senha, token))
                existUser = True

        if not existUser:
            params = (str(matricula), str(senha), str(token))
            cursor.execute("""
            INSERT INTO users 
            VALUES (null, ?, ?, ?)
            """, params)
        conn.commit()
        conn.close()

    return { 'Status':loged, 'name':name, 'token':token }