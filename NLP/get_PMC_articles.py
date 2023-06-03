# SOURCE: https://www.youtube.com/watch?v=_M3Cndj7MpY&t=883s

# Importing the necessary modules
from requests_html import HTMLSession
import requests
from requests.exceptions import ConnectionError

# Creating an HTML session object
s = HTMLSession()

# Setting the user-agent header for the requests
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'}

# Opening the input file
file = open('input.txt', 'r')

# Reading the lines from the input file
ids = file.readlines()

# Iterating over each line in the input file
for pmc in ids:
    try: 
        # Stripping any whitespace or newline characters from the current line
        pmcid = pmc.strip()
        
        # Constructing the base URL for the PMC article
        base_url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
        
        # Sending a GET request to the PMC article URL with specified headers and timeout
        r = s.get(base_url + pmcid + '/', headers=headers, timeout=5)
        
        # Extracting the URL for the PDF file from the response HTML
        pdf_url = 'https://www.ncbi.nlm.nih.gov' + r.html.find('a.int-view', first=True).attrs['href']
        
        # Printing the PDF URL
        print(pdf_url) 
        
        # Sending a GET request to the PDF URL with stream=True to enable streaming response
        r = s.get(pdf_url, stream=True)
        
        # Saving the PDF content to a file
        with open(pmcid + '.pdf', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except ConnectionError as e:
        # If a ConnectionError occurs, ignore and continue to the next PMC ID
        pass
        out = open('ConnectionError_pmcids.txt', 'a')
        out.write(pmcid + '\n')
