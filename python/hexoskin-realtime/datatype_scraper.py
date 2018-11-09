from bs4 import BeautifulSoup
from requests import get

file = open('constants.py', 'a')
url = "https://api.hexoskin.com/docs/resource/datatype/"
content = get(url, stream=True).content
html = BeautifulSoup(content)
rows = html.select('tr')

for row in rows:
    cells = row.select('td')

    if len(cells) > 0:
        data_name = cells[0].select('a')[0].contents[0]
        data_type = cells[1].contents[0]
        file.write(data_name + " = " + str(data_type) + "\n")
