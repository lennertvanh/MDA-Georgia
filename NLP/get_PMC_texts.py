from requests_html import HTMLSession
import requests
from requests.exceptions import ConnectionError

s = HTMLSession()

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'}

file = open('input.txt', 'r')
ids = file.readlines()
for pmc in ids:
    try: 
        pmcid = pmc.strip()
        base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
        r = s.get(base_url + pcmid + '/', headers=headers, timeout=5)
        pdf_url = 'https://www.ncbi.nlm.nih.gov' + r.html.find('a.int-view', first=True).attrs['href']
        print(pdf_url) 
        r = s.get(pdf_url, stream=True)
        with open(pmcid + '.pdf', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except ConnectionError as e:
        pass
        out = open('ConnectionError_pmcids.txt', 'a')
        out.write(pmcid + '\n')
