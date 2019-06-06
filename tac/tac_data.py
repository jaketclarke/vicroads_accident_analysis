from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
from tac_db import PostgresDB
from datetime import timedelta, date
from collections import namedtuple
from io import StringIO

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# datefrom = date(1987, 4, 27)
# dateto = date(2019, 6, 1)

datefrom = date(2000,5,1)
dateto=date(2000,5,2)

db = PostgresDB()
db.createTacDataRawIfNotExists()

for single_date in daterange(datefrom, dateto):
    startdate = single_date
    # enddate = single_date + timedelta(days=1)
    enddate = single_date
    
    # params for url
    params = {'meta_J_orsand':'','meta_G_orsand':'','query':'!padrenull','collection':'tac-xml-meta','clive':'tac-fatalities-xml'}

    # from and to
    params['date-after'] = startdate.strftime('%d-%b-%Y')
    params['date-before']= enddate.strftime('%d-%b-%Y')
   
    # we need to do two steps
    # step 1 is getting an initial page
    # on the loading of step 1, it gets some stuff that it sends to page 2, so we need to load them in order, then get the element we want from page 2
    url = 'http://reporting.tacsafety.com.au/s/search.html?{0}'.format(urlencode(params))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')

    # we want to find the link from this page to page 2, which is the first gray-btn-primary
    magic = soup.find('a', {'class':'gray-btn-primary'}, href=True )['href'].strip()
    url2 = 'http://reporting.tacsafety.com.au/s/search.html{0}'.format(magic)
    
    # we then want to grab page 2, and get hte 'csv_data part of it
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.text, 'html5lib')
    results = soup2.find('input', {'name': 'csv_data'})

    # need to make this a function for ease of reading
    # loop through each line in this data, and format for db, then insert at the end
    data = []
    datastr = ''
    RowObj = namedtuple('RowObj', ['startdate', 'enddate', 'needle', 'val'])

    rows = str(results).splitlines()

    startdate = startdate.strftime('%Y-%m-%d')
    enddate = enddate.strftime('%Y-%m-%d')

    for row in rows:
        columns = row.split(',')
        needle = columns[0]
        val = ''
        if len(columns) > 1:
            val = columns[1]

        datastr += '{0}\t{1}\t{2}\t{3}\n'.format(startdate,enddate,needle,val.strip())

    print(datastr)
    datastr = datastr.rstrip('\n')
    datastr = StringIO(datastr)
    print(datastr)
    db.bulkinsert(datastr)