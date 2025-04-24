from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------- CONFIGURAÇÕES DO EMAIL --------
EMAIL_ORIGEM = 'gabrielalvesdevv@gmail.com'
EMAIL_DESTINO = 'gaa.alves74@gmail.com'
SENHA_APP = '-'  # sua senha de app gerada no Gmail

# -------- WEBSCRAPER COM SELENIUM --------
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)

try:
    driver.get('https://tempoagora.uol.com.br/')
    time.sleep(5)  # Espera a página carregar

    # Coletando a previsão de hoje
    temperatura = driver.find_element(By.XPATH, '//*[@id="current-weather-temperature"]').text
    condicao = driver.find_element(By.XPATH, '//*[@id="current-weather-condition"]').text

    # Coletando a previsão de amanhã
    temp_amanha = driver.find_element(By.XPATH, '//div[contains(@class, "card") and .//p[text()="Amanhã"]]//span[contains(text(), "Temperatura")]/following::p[1]').text

    # Coletando a previsão para sábado
    temp_sabado = driver.find_element(By.XPATH, '//div[contains(@class, "card") and .//p[text()="Sábado"]]//span[contains(text(), "Temperatura")]/following::p[1]').text

    print(f'Temperatura atual: {temperatura}')
    print(f'Condição atual: {condicao}')
    print(f"Temperatura mínima e máxima de amanhã: {temp_amanha}")
    print(f"Temperatura mínima e máxima de sábado: {temp_sabado}")

    # -------- MONTANDO O EMAIL --------
    assunto = "Previsão do Tempo - São Paulo"
    corpo = f"""Olá!

Aqui está a previsão do tempo para São Paulo:

🌡 **Temperatura Atual:** {temperatura}
🌥 **Condição Atual:** {condicao}

🌞 **Temperatura de Amanhã:** {temp_amanha}

🌤 **Temperatura de Sábado:** {temp_sabado}

Tenha um ótimo dia! ☀️
"""

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = EMAIL_DESTINO
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    # -------- ENVIANDO O EMAIL --------
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ORIGEM, SENHA_APP)
        server.send_message(msg)
        print("✅ E-mail enviado com sucesso!")

finally:
    driver.quit()
