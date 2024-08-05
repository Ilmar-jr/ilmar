from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from bs4 import BeautifulSoup
import pyautogui

def webscraping():

    # login
    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico)

    driver.get('https://espacolaser.evup.com.br/Login')
    time.sleep(3)
    driver.find_element(By.ID,'Login').send_keys('11902545737')
    time.sleep(3)
    driver.find_element(By.ID,'Password').send_keys('Lucasmanuph*24')
    time.sleep(3)
    driver.find_element(By.XPATH,'/html/body/div[2]/form/div[2]/button').click()
    time.sleep(15)

    for i in range(1,20):
        try:
            driver.find_element(By.XPATH,f'/html/body/div[{i}]/button').click()
            time.sleep(1)
        except:
            pass

    a = 20
    for i in range(0,20):
        valor = a - i
        try:
            driver.find_element(By.XPATH,f'/html/body/div[{valor}]/button').click()
            time.sleep(1)
        except:
            pass

       

    # forma de pagamento e vendedor
    driver.find_element(By.XPATH,'//*[@id="page-menu-container"]/div/div/div/ul/li[5]/a/i').click()
    time.sleep(5)
    driver.find_element(By.XPATH,'//*[@id="menucol2"]/div[2]/div[2]/div/div/div/ul/li[8]/div/span/a').click()
    time.sleep(5)
    driver.find_element(By.ID,'s2id_autogen3').send_keys('forma de pagamento')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)
    driver.find_element(By.ID,'s2id_autogen3').send_keys('Vendedor')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(15)


    # data
    driver.find_element(By.XPATH,'//*[@id="txtDate"]').clear()
    driver.find_element(By.XPATH,'//*[@id="txtDate"]').send_keys('01/08/2024 - 01/08/2024')
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)
    driver.find_element(By.ID,'btnFilter').click()
    time.sleep(5)
    driver.find_element(By.CLASS_NAME,'k-icon.k-i-expand').click()
    time.sleep(5)


    html = driver.page_source.encode('utf-8')

    soup = BeautifulSoup(html)

    # mydivs = soup.find_all("div", {"data-role": "k-grid.k-widget.k-display-block.loaded"})
    mydivs = soup.find_all("td",{'role':'gridcell'})


    resultado = []
    for j,i in enumerate(mydivs):
        #print(j,mydivs[0].text)
        if '/' in i.get_text():
            resultado.append([mydivs[j].text,mydivs[j+11].text,mydivs[j+12].text,mydivs[j+13].text,
                            mydivs[j+14].text,mydivs[j+23].text,mydivs[j+24].text,mydivs[j+25].text,
                            mydivs[j+26].text,mydivs[j+27].text])
                
    tabela = pd.DataFrame(resultado)

    tabela = tabela.rename(columns={0:'Data Pagamento',1:'Vendedor',2:'perfil',3:'cargo',4:'cpf',5:'vl bruto',
                                6:'vl desconto',7:'vl líquido',8:'forma de pagamento',9:'condição de pagamento'})

    def numero(valor):
        valor = str(valor)
        valor = valor.replace('R$','')
        valor = valor.replace('.','')
        valor = valor.replace(',','.')
        return valor

    tabela['Data Pagamento'] = pd.to_datetime(tabela['Data Pagamento'],format="%d/%m/%Y")
    tabela['vl bruto'] = tabela['vl bruto'].apply(lambda x:numero(x))
    tabela['vl bruto'] = pd.to_numeric(tabela['vl bruto'])

    tabela['vl desconto'] = tabela['vl desconto'].apply(lambda x:numero(x))
    tabela['vl desconto'] = pd.to_numeric(tabela['vl desconto'])

    tabela['vl líquido'] = tabela['vl líquido'].apply(lambda x:numero(x))
    tabela['vl líquido'] = pd.to_numeric(tabela['vl líquido'])

    return tabela