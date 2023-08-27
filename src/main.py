import csv
import re
import requests
from bs4 import BeautifulSoup

url = "https://myanimelist.net/topmanga.php"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    mangas = soup.find_all(class_="ranking-list")

    file = open('data/manga.csv', 'w', newline='')
    writer = csv.writer(file)
    headers = ['Name', 'Volumes', 'Score']

    writer.writerow(headers)

    for manga in mangas:
        name = manga.find(class_="hoverinfo_trigger fs14 fw-b").get_text()
        score = manga.find(class_=re.compile(r"text on score-label score-([1-9])")).get_text()
        detail = manga.find(class_="information di-ib mt4").get_text()
        detail = re.sub("\n", '', detail)
        vols = re.sub(r'(.*\(|\).*)', '', detail, re.MULTILINE)
        if vols == "? vols":
            vols = "on going"
        writer.writerow([name] + [vols] + [score])
        print(name + ' - '  + vols + ', ' + score )
else:
    print("erro")