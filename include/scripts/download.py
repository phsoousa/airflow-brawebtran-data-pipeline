import os
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By


USUARIO = os.getenv("WEBTRAN_USER")
SENHA = os.getenv("WEBTRAN_PASS")
CODTRAN = os.getenv("WEBTRAN_CODTRAN", "SSCFRWX9")

BASE_DOWNLOAD = Path("/usr/local/airflow/desktop_downloads")
PASTA_DIA = BASE_DOWNLOAD / datetime.now().strftime("%Y-%m-%d")
PASTA_DIA.mkdir(parents=True, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

options.add_experimental_option("prefs", {
    "download.default_directory": str(PASTA_DIA),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})

driver = webdriver.Chrome(options=options)

try:
    url = f"https://{USUARIO}:{SENHA}@os390.bradescoseguros.com.br/suporte/WebTran.html"
    driver.get(url)

    time.sleep(5)

    driver.switch_to.frame("banner")
    driver.find_element(By.LINK_TEXT, "Recepção de Arquivos").click()

    print("Login realizado com sucesso.")

    time.sleep(3)

    driver.switch_to.default_content()
    driver.switch_to.frame("corpo")

    driver.find_element(By.NAME, "CODTRAN").send_keys(CODTRAN)
    driver.find_element(By.NAME, "Submit").click()

    time.sleep(10)

    print(f"Processo finalizado. Arquivos salvos em: {PASTA_DIA}")

except Exception as erro:
    alerta_path = BASE_DOWNLOAD / "alerta_erro.txt"

    with open(alerta_path, "w", encoding="utf-8") as arquivo:
        arquivo.write("Falha na automação WebTran.\n")
        arquivo.write("O processo foi interrompido na primeira tentativa.\n")
        arquivo.write("Nenhuma nova tentativa foi feita para evitar bloqueio do usuário.\n")
        arquivo.write(f"Erro: {erro}\n")

    print("Falha na automação. Alerta gerado.")
    raise

finally:
    driver.quit()