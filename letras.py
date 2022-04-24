import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options

class Scraping:
    def __init__(self):
        self.lista_musicas = []

    def iniciar(self):
        self.abrir_site()
        self.criar_arquivo()

    def abrir_site(self):
        self.options = Options()
        self.banda = input('Qual banda deseja pesquisar? ')
        self.options.add_argument('--headless')
        self.navegador = webdriver.Chrome(options=self.options)

        # Entrar na pagina de musicas da banda escolhida
        self.navegador.get(f'https://www.letras.mus.br/{self.banda}/')
        sleep(2)

        # Clicar no botão de "ver tudo", para aparecer todas as musicas na página
        ver_todos = self.navegador.find_element_by_css_selector('a[data-art-action="Click Ver Mais"]')
        ver_todos.click()
        sleep(2)

        self.hrefs = self.navegador.find_elements_by_css_selector('a[class="song-name"]')
        self.links_hrefs = [self.elem.get_attribute('href') for self.elem in self.hrefs]

        for self.href in self.links_hrefs:
            self.navegador.get(self.href)
            self.raspagem()
    
    def raspagem(self):
        sleep(2)
        self.site = BeautifulSoup(self.navegador.page_source, 'html.parser')

        self.titulo = self.site.find('div', attrs={'class': 'cnt-head_title'}).find('h1')

        self.letra = self.site.find('div', attrs={'class': 'cnt-letra p402_premium'})

        self.frases = self.letra.findAll('p')
        self.frases = ''.join([self.frase.text for self.frase in self.frases])
        self.lista_musicas.append([self.titulo.text, self.frases])
    
    def criar_arquivo(self):
        self.dados = pd.DataFrame(self.lista_musicas, columns=['titulo', 'letra'])
        
        self.dados.to_excel(f'Musicas: {self.banda}.xlsx', index=False)


letras = Scraping()
letras.iniciar()