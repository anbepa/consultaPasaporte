from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Configurar Selenium para ejecutarse en modo normal (navegador visible)
chrome_options = Options()
chrome_options.add_argument('--headless')  # Ejecutar en modo headless
chrome_options.add_argument('--disable-gpu')  # Necesario para algunos entornos headless
chrome_options.add_argument('--no-sandbox')  # Necesario para algunos entornos CI/CD
chrome_options.add_argument('--disable-dev-shm-usage')  # Evitar problemas con recursos de memoria compartida
chrome_options.add_argument('--window-size=1920x1080')  # Opcional: establecer un tamaño de ventana fijo
chrome_options.add_argument('--remote-debugging-port=9222')  # Para depuración remota si es necesario

# Inicializar el WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Función para enviar correo electrónico
def enviar_correo(asunto, mensaje, archivo=None):
    remitente = "andro11anto@gmail.com"
    destinatario = "andro11anto@gmail.com"
    password = "vfri bmrw zxkn otrj"

    # Configuración del mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    # Adjuntar el archivo si se proporciona uno
    if archivo:
        attachment = open(archivo, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(archivo)}")
        msg.attach(part)
        attachment.close()

    # Conectar al servidor de Gmail y enviar el correo
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# URL de la página que deseas abrir
url = "https://pasaportesatlantico.gov.co/#"
driver.get(url)

# Realizar clics necesarios en el flujo
try:
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#alert_version_52 > div > div > div.modal-header > button'))
    )
    button.click()
    print("Botón clicado con éxito.")
except Exception as e:
    print("Error al intentar clicar el botón:", e)

try:
    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > section > div.tabla1.tablaBloque27.container.acordeon > div > div > label'))
    )
    label.click()
    print("Clic en el label realizado con éxito.")
except Exception as e:
    print("Error al intentar clicar el label:", e)

try:
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > section > div.tabla1.tablaBloque27.container.acordeon > div > div > div.tab-content > p:nth-child(4) > a'))
    )
    link.click()
    print("Clic en el enlace realizado con éxito.")
except Exception as e:
    print("Error al intentar clicar el enlace:", e)

# Esperar unos segundos para que la página se cargue después del último clic
time.sleep(5)

# Verificar si la alerta está presente
alerta_presente = False
try:
    alerta = driver.find_element(By.CSS_SELECTOR, '#infoPrincipal > div.modContent > div.msgError.alert.alert-danger.alert-dismissable')
    alerta_presente = True
except:
    alerta_presente = False

# Tomar una captura de pantalla
screenshot_path = "captura_pagina.png"
driver.save_screenshot(screenshot_path)
print(f"Captura de pantalla guardada en {screenshot_path}")

# Enviar correo dependiendo de si la alerta está presente
if alerta_presente:
    enviar_correo("Alerta en la página", "Aún persiste el error.", archivo=screenshot_path)
else:
    enviar_correo("Todo está bien", "Ya está bien, puedes proseguir.", archivo=screenshot_path)

# Cerrar el navegador
driver.quit()
