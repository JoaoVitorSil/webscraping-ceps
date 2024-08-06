import pandas as pd
import gdown
import requests
from bs4 import BeautifulSoup

url = 'https://drive.google.com/file/d/1sbpVvn6tVmdWoO_JqpXQ9UegaszHAl7M/view?usp=sharing'
output = 'cep_filtrados.csv'
gdown.download(url=url, output=output, quiet=False, fuzzy=True)

data = pd.read_csv('cep_filtrados.csv')
logradouros = list()
bairros = list()

headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

for i in range(len(data["CEP"])):
    url2 = "https://buscacep.com.br/cep/"+str(data['CEP'][i])
    site = requests.get(url2, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    tag = soup.find("td", {"id": "logradouroTd"})
    logradouro = tag.get_text().strip()
    logradouros.append(logradouro)
    tag2 = soup.find("td", {"id": "bairroTd"})
    bairro = tag2.get_text().strip()
    bairros.append(bairro)

data["LOGRADOURO"] = logradouros
data["BAIRRO"] = bairros

data.to_csv("ceps_add_lograd_bairro.csv",index=False)
print(data.to_string())
