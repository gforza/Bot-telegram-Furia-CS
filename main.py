import telebot
import requests
import time
from selenium import webdriver 
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

bot = telebot.TeleBot('Coloque o token do bot aqui')

def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=chrome_options)

@bot.message_handler(commands=['start'])
def iniciar_conversa(msg):
    texto = """Bem-vindo ao Bot da FURIA! 🐆

Escolha uma das opções abaixo:

1️⃣ /Sobre - Conheça a história da FURIA no CS
2️⃣ /Jogadores - Veja a line atual do time
3️⃣ /Estatisticas - Estatísticas do time
4️⃣ /Proximos_eventos - Próximos campeonatos
5️⃣ /Proximas_partidas - Próximas partidas
6️⃣ /Resultados - Últimos resultados
7️⃣ /Noticias - Últimas notícias da FURIA

Para ajuda, digite /Ajuda"""
    bot.reply_to(msg, texto)

@bot.message_handler(commands=['Sobre'])
def sobre(msg):
    historia_texto = """A FURIA é uma organização brasileira de esports fundada em 2017. 
    
No CS:GO, a FURIA se destacou por seu estilo agressivo e inovador de jogo, foi crescendo de pouco em pouco, conquistando diversos títulos importantes
e se tornou uma das principais forças do cenário internacional, virando o melhor time do Brasil 🐆🇧🇷.

Alguns marcos importantes:
- 2018: Entrada no cenário competitivo
- 2019: Primeiras conquistas internacionais
- 2020: Consolidação como time top 10 mundial
- 2021-2023: Manutenção entre os melhores times do mundo
"""
    bot.reply_to(msg, historia_texto)

@bot.message_handler(commands=['Jogadores'])
def jogadores(msg):
    texto = """Escolha uma das opções abaixo:\n\n1️⃣ /LineNomes - Ver nomes da line atual\n2️⃣ /LineFotos - Ver fotos dos jogadores"""
    bot.reply_to(msg, texto)

@bot.message_handler(commands=['LineNomes'])
def line_nomes(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando informações...")
    try:
        driver = setup_selenium()
        driver.get('https://www.hltv.org/team/8297/furia')
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.bodyshot-team.g-grid a.col-custom'))
        )
        jogadores = driver.find_elements(By.CSS_SELECTOR, '.bodyshot-team.g-grid a.col-custom')
        resposta = "🐆 Line atual da FURIA:\n\n"
        if not jogadores:
            resposta += "Não foi possível encontrar os jogadores."
        else:
            for jogador in jogadores:
                nome = jogador.get_attribute("title")
                if nome:
                    resposta += f"\U0001F464 {nome}\n"
        driver.quit()
        resposta = resposta.strip()
        bot.reply_to(msg, resposta)
    except Exception as e:
        print(f"Erro completo: {str(e)}")
        bot.reply_to(msg, f"Desculpe, não foi possível obter os nomes da line. Erro: {str(e)}")

@bot.message_handler(commands=['LineFotos'])
def line_fotos(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando informações...")
    try:
        driver = setup_selenium()
        driver.get('https://www.hltv.org/team/8297/furia')
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.bodyshot-team.g-grid a.col-custom'))
        )
        jogadores = driver.find_elements(By.CSS_SELECTOR, '.bodyshot-team.g-grid a.col-custom')
        if not jogadores:
            bot.reply_to(msg, "Não foi possível encontrar os jogadores.")
        else:
            for jogador in jogadores:
                nome = jogador.get_attribute("title")
                foto_url = None
                try:
                    img_tag = jogador.find_element(By.CSS_SELECTOR, 'div.overlayImageFrame img')
                    foto_url = img_tag.get_attribute("src")
                except Exception:
                    foto_url = None
                if nome and foto_url:
                    bot.send_photo(msg.chat.id, foto_url, caption=f"{nome}")
                elif nome:
                    bot.send_message(msg.chat.id, f"👤 {nome}")
        driver.quit()
    except Exception as e:
        print(f"Erro completo: {str(e)}")
        bot.reply_to(msg, f"Desculpe, não foi possível obter as fotos da line. Erro: {str(e)}")

@bot.message_handler(commands=['Estatisticas'])
def estatisticas(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando informações...")
    texto = """Escolha uma opção:

1️⃣ /mapas - Estatísticas por mapa"""
    bot.reply_to(msg, texto)

@bot.message_handler(commands=['mapas'])
def estatisticas_mapas(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando informações...")
    try:
        driver = setup_selenium()
        driver.get('https://www.hltv.org/team/8297/furia#tab-statsBox')
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.map-statistics-container .map-statistics-row'))
        )
        mapas = driver.find_elements(By.CSS_SELECTOR, '.map-statistics-container .map-statistics-row')
        resposta = "🗺️ Estatísticas por mapa (últimos 3 meses):\n\n"
        if not mapas:
            resposta += "Nenhuma estatística encontrada."
        else:
            for mapa in mapas:
                try:
                    nome_mapa = mapa.find_element(By.CLASS_NAME, "map-statistics-row-map-mapname").text
                    win_rate = mapa.find_element(By.CLASS_NAME, "map-statistics-row-win-percentage").text
                    if nome_mapa and win_rate:
                        resposta += f"{nome_mapa}: {win_rate}\n"
                except Exception as e:
                    print(f"Erro ao processar mapa: {str(e)}")
        driver.quit()
        resposta = resposta.strip()
        bot.reply_to(msg, resposta)
    except Exception as e:
        print(f"Erro completo: {str(e)}")
        bot.reply_to(msg, f"Desculpe, não foi possível obter as estatísticas dos mapas. Erro: {str(e)}")

@bot.message_handler(commands=['Proximos_eventos'])
def proximos_eventos(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando informações...")
    try:
        driver = setup_selenium()
        driver.get('https://www.hltv.org/team/8297/furia#tab-eventsBox')
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.a-reset.ongoing-event'))
        )
        eventos = driver.find_elements(By.CSS_SELECTOR, 'a.a-reset.ongoing-event')
        resposta = "🏆 Próximos eventos da FURIA:\n\n"
        count = 0
        for evento in eventos:
            if count >= 5:
                break
            try:
                nome_evento = evento.find_element(By.CLASS_NAME, "eventbox-eventname").text
                data = evento.find_element(By.CLASS_NAME, "eventbox-date").text
                if nome_evento and data:
                    resposta += f"📅 {data}\n🏆 {nome_evento}\n\n"
                    count += 1
            except Exception as e:
                print(f"Erro ao processar evento: {str(e)}")
        driver.quit()
        resposta = resposta.strip()  # Remove quebras de linha extras no final
        bot.reply_to(msg, resposta)
    except Exception as e:
        print(f"Erro completo: {str(e)}")
        bot.reply_to(msg, f"Desculpe, não foi possível obter os próximos eventos. Erro: {str(e)}")

@bot.message_handler(commands=['Proximas_partidas'])
def proximas_partidas(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando informações...")
    try:
        driver = setup_selenium()
        driver.get('https://www.hltv.org/team/8297/furia#tab-matchesBox')
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h2.standard-headline'))
        )
        h2s = driver.find_elements(By.CSS_SELECTOR, 'h2.standard-headline')
        tabela_proximas = None
        for h2 in h2s:
            if 'Upcoming matches for FURIA' in h2.text:
                tabela_proximas = h2.find_element(By.XPATH, 'following-sibling::table[1]')
                break
        if not tabela_proximas:
            bot.reply_to(msg, 'Não foi possível encontrar a tabela de próximas partidas.')
            driver.quit()
            return
        theads = tabela_proximas.find_elements(By.TAG_NAME, 'thead')
        tbodys = tabela_proximas.find_elements(By.TAG_NAME, 'tbody')
        resposta = "⏳ Próximas partidas da FURIA:\n"
        count = 0
        for thead, tbody in zip(theads[1:], tbodys):
            try:
                camp = thead.find_element(By.XPATH, './/a[contains(@class, "a-reset")]').text
                resposta += f"\n*{camp}*\n"
            except Exception as e:
                print(f"Erro ao buscar nome do campeonato: {str(e)}")
                continue
            linhas = tbody.find_elements(By.CSS_SELECTOR, 'tr.team-row')
            for linha in linhas:
                try:
                    data = linha.find_element(By.CSS_SELECTOR, '.date-cell span[data-time-format]').text
                    time1 = linha.find_element(By.CSS_SELECTOR, '.team-center-cell .team-name.team-1').text
                    time2 = linha.find_element(By.CSS_SELECTOR, '.team-flex:last-child .team-name.team-2').text
                    score_cell = linha.find_element(By.CSS_SELECTOR, '.score-cell')
                    scores = score_cell.find_elements(By.CSS_SELECTOR, '.score')
                    score1 = scores[0].text if len(scores) > 0 else '-'
                    score2 = scores[1].text if len(scores) > 1 else '-'
                    resposta += f"{data} | {time1} {score1} x {score2} {time2}\n"
                    count += 1
                except Exception as e:
                    print(f"Erro ao processar partida: {str(e)}")
                if count >= 10:
                    break
            if count >= 10:
                break
        driver.quit()
        resposta = resposta.strip()
        bot.reply_to(msg, resposta, parse_mode='Markdown')
    except Exception as e:
        print(f"Erro completo: {str(e)}")
        bot.reply_to(msg, f"Desculpe, não foi possível obter as próximas partidas. Erro: {str(e)}")

@bot.message_handler(commands=['Resultados'])
def resultados(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando informações...")
    try:
        driver = setup_selenium()
        driver.get('https://www.hltv.org/team/8297/furia#tab-matchesBox')
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h2.standard-headline'))
        )
        h2s = driver.find_elements(By.CSS_SELECTOR, 'h2.standard-headline')
        tabela_resultados = None
        for h2 in h2s:
            if 'Recent results for FURIA' in h2.text:
                tabela_resultados = h2.find_element(By.XPATH, 'following-sibling::table[1]')
                break
        if not tabela_resultados:
            bot.reply_to(msg, 'Não foi possível encontrar a tabela de resultados recentes.')
            driver.quit()
            return
        theads = tabela_resultados.find_elements(By.TAG_NAME, 'thead')
        tbodys = tabela_resultados.find_elements(By.TAG_NAME, 'tbody')
        resposta = "📊 Últimos resultados da FURIA:\n"
        count = 0
        for thead, tbody in zip(theads[1:], tbodys):
            try:
                camp = thead.find_element(By.XPATH, './/a[contains(@class, "a-reset")]').text
                resposta += f"\n*{camp}*\n"
            except Exception as e:
                print(f"Erro ao buscar nome do campeonato: {str(e)}")
                continue
            linhas = tbody.find_elements(By.CSS_SELECTOR, 'tr.team-row')
            for linha in linhas:
                try:
                    data = linha.find_element(By.CSS_SELECTOR, '.date-cell span[data-time-format]').text
                    time1 = linha.find_element(By.CSS_SELECTOR, '.team-center-cell .team-name.team-1').text
                    time2 = linha.find_element(By.CSS_SELECTOR, '.team-flex:last-child .team-name.team-2').text
                    score_cell = linha.find_element(By.CSS_SELECTOR, '.score-cell')
                    scores = score_cell.find_elements(By.CSS_SELECTOR, '.score')
                    if len(scores) >= 2:
                        score1 = scores[0].text
                        score2 = scores[1].text
                        resposta += f"{data} | {time1} {score1} x {score2} {time2}\n"
                        count += 1
                except Exception as e:
                    print(f"Erro ao processar partida: {str(e)}")
                if count >= 20:
                    break
            if count >= 20:
                break
        driver.quit()
        resposta = resposta.strip()
        bot.reply_to(msg, resposta, parse_mode='Markdown')
    except Exception as e:
        print(f"Erro completo: {str(e)}")
        bot.reply_to(msg, f"Desculpe, não foi possível obter os resultados. Erro: {str(e)}")

@bot.message_handler(commands=['Ajuda'])
def ajuda(msg):
    texto = """Comandos disponíveis:

/start - Inicia o bot
/Sobre - História da FURIA no CS
/Jogadores - Line atual do time
/Estatisticas - Menu de estatísticas
/Mapas - Estatísticas por mapa
/Proximos_eventos - Próximos campeonatos
/Proximas_partidas - Próximas partidas
/Resultados - Últimos resultados
/Noticias - Últimas notícias da FURIA
/Ajuda - Mostra esta mensagem de ajuda"""
    bot.reply_to(msg, texto)

@bot.message_handler(commands=['Noticias'])
def noticias(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando as últimas notícias...")
    try:
        driver = setup_selenium()
        driver.get('https://themove.gg/esports/cs')
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-test-id="story-card"]'))
        )
        cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="story-card"]')[:4]
        resposta = '📰 Últimas notícias da FURIA (fonte: themove.gg):\n\n'
        for card in cards:
            # Título
            titulo = 'Sem título'
            link = ''
            try:
                headline = card.find_element(By.CSS_SELECTOR, 'div[data-test-id="headline"]')
                try:
                    titulo = headline.find_element(By.TAG_NAME, 'h6').text.strip()
                except:
                    titulo = headline.find_element(By.TAG_NAME, 'h5').text.strip()
                try:
                    a_tag = headline.find_element(By.TAG_NAME, 'a')
                    link = a_tag.get_attribute('href')
                except:
                    link = ''
            except:
                pass
            # Fonte
            fonte = 'Sem fonte'
            try:
                fonte = card.find_element(By.CSS_SELECTOR, 'div[data-test-id="author-name"]').text.strip()
            except:
                pass
            # Data
            data = 'Sem data'
            try:
                data = card.find_element(By.CSS_SELECTOR, 'div[data-test-id="publish-time"] time').text.strip()
            except:
                pass
            resposta += f'• <b>{titulo}</b>\nFonte: {fonte}\nData: {data}'
            if link:
                resposta += f'\n<a href="{link}">[Abrir notícia]</a>'
            resposta += '\n\n'
        resposta += 'Para ver mais notícias, digite /MaisNoticias'
        driver.quit()
        bot.reply_to(msg, resposta, parse_mode='HTML')
    except Exception as e:
        print(f"Erro ao buscar notícias: {str(e)}")
        bot.reply_to(msg, f"Desculpe, não foi possível obter as notícias. Erro: {str(e)}")

@bot.message_handler(commands=['MaisNoticias'])
def mais_noticias(msg):
    aviso = bot.reply_to(msg, "⏳ Aguarde um momento, buscando mais notícias...")
    try:
        texto = msg.text.strip().split()
        offset = 4
        if len(texto) > 1 and texto[1].isdigit():
            offset = int(texto[1])
        driver = setup_selenium()
        driver.get('https://themove.gg/esports/cs')
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-test-id="story-card"]'))
        )
        cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="story-card"]')[offset:offset+4]
        if not cards:
            bot.reply_to(msg, "Não há mais notícias para mostrar.")
            driver.quit()
            return
        resposta = f'📰 Mais notícias da FURIA (de {offset+1} a {offset+len(cards)}):\n\n'
        for card in cards:
            # Título
            titulo = 'Sem título'
            link = ''
            try:
                headline = card.find_element(By.CSS_SELECTOR, 'div[data-test-id="headline"]')
                try:
                    titulo = headline.find_element(By.TAG_NAME, 'h6').text.strip()
                except:
                    titulo = headline.find_element(By.TAG_NAME, 'h5').text.strip()
                try:
                    a_tag = headline.find_element(By.TAG_NAME, 'a')
                    link = a_tag.get_attribute('href')
                except:
                    link = ''
            except:
                pass
            # Fonte
            fonte = 'Sem fonte'
            try:
                fonte = card.find_element(By.CSS_SELECTOR, 'div[data-test-id="author-name"]').text.strip()
            except:
                pass
            # Data
            data = 'Sem data'
            try:
                data = card.find_element(By.CSS_SELECTOR, 'div[data-test-id="publish-time"] time').text.strip()
            except:
                pass
            resposta += f'• <b>{titulo}</b>\nFonte: {fonte}\nData: {data}'
            if link:
                resposta += f'\n<a href="{link}">[Abrir notícia]</a>'
            resposta += '\n\n'
        driver.quit()
        bot.reply_to(msg, resposta, parse_mode='HTML')
    except Exception as e:
        print(f"Erro ao buscar mais notícias: {str(e)}")
        bot.reply_to(msg, f"Desculpe, não foi possível obter mais notícias. Erro: {str(e)}")

bot.infinity_polling()
