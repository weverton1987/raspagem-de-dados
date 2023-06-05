

from requests_html import HTMLSession
import sqlite3
sessao = HTMLSession()
url = 'https://www.olx.com.br/imoveis/estado-mg/belo-horizonte-e-regiao/pampulha'
imoveis = []
resposta = sessao.get(url)
links = resposta.html.find('#ad-list li a')
for link in links:
    url_imovel = link.attrs['href']
    resposta_imovel = sessao.get(url_imovel)
    titulo = resposta_imovel.html.find('h1', first=True).text
    preco = resposta_imovel.html.find('h2')[0].text
    imoveis.append({
        'url': url_imovel,
        'titulo': titulo,
        'preço': preco
    })
print(imoveis)
conexao = sqlite3.connect('bancojunho')
cursor = conexao.cursor()
cursor.execute('''CREATE TABLE imoveis (id integer not null primary key autoincrement, url VARCHAR (200),
titulo VARCHAR (200), preço VARCHAR (200))''')
sql = ('INSERT INTO imoveis (url, titulo, preço) values (?, ?, ?)')
for imovel in imoveis:
    valores = [imovel['url'], imovel['titulo'], imovel['preço']]
    cursor.execute(sql, valores)
conexao.commit()
conexao.close()