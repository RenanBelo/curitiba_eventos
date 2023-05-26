from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, JavascriptException
import json
import time

url = "https://cheersapp.com.br/eventos"

driver = webdriver.Chrome()
driver.get(url)

wait = WebDriverWait(driver, 10)

eventos_info = []
for i in range(1, 11):
    seletor = "#eventoswindow > div:nth-child(8) > div:nth-child({})".format(i)
    evento = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
    
    # Rolando a página até que o evento esteja visível
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", evento)
    time.sleep(1)  # Esperando a rolagem ser concluída
    
    try:
        evento.click()
        time.sleep(2)
        try:
            nome_evento = driver.find_element_by_css_selector("#app > div.container > div > div > div:nth-child(1) > div.col-md-7 > p").text
            data_horario_elements = driver.find_elements_by_css_selector("#app > div.container > div > div > div:nth-child(2) > div:nth-child(1) > div > div > p:nth-child(2), #app > div.container > div > div > div:nth-child(2) > div:nth-child(1) > div > div > p:nth-child(3)")
            data_horario = " ".join([element.text for element in data_horario_elements])
            endereco_local = driver.find_element_by_css_selector("#app > div.container > div > div > div:nth-child(2) > div:nth-child(2) > div > div > a").text
            eventos_info.append({
                "nome_evento": nome_evento,
                "data_horario": data_horario,
                "endereco_local": endereco_local
            })
        except NoSuchElementException:
            pass
        driver.back()
        time.sleep(8)
    except JavascriptException:
        pass

with open("eventos_teste.json", "w", encoding="utf-8") as f:
    json.dump(eventos_info, f, ensure_ascii=False)

driver.quit()
