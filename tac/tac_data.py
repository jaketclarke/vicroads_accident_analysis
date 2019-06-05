from bs4 import BeautifulSoup
import requests

url = 'http://reporting.tacsafety.com.au/s/search.html?collection=tac-xml-meta&query=!padrenull&clive=tac-fatalities-xml&meta_d3day=1&meta_d3month=Jan&meta_d3year=1987&meta_d4day=1&meta_d4month=Jun&meta_d4year=2019&meta_G_orsand=&meta_J_orsand=&form=template-download&previous_form=simple'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')

data = soup.find('input',{
    'name': 'csv_data'
})

rows = str(data).splitlines()

for row in rows:
    print(row)
    print('|')