import requests
from bs4 import BeautifulSoup
import urllib.parse

url = "https://www.cert.ssi.gouv.fr/avis/CERTFR-2023-AVI-0352/"

parsed_url = urllib.parse.urlparse(url)
path_elements = parsed_url.path.strip('/').split('/')
name = path_elements[-1]

response = requests.get(url)

if response.status_code == 200:
    html_content = response.content.decode("utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    
    table = soup.find("table", class_="table table-condensed")

    table_rows = table.find_all("tr")

    info = {}

    for row in table_rows:
        header = row.find("td", class_="col-xs-4").text
        value = row.find("td", class_="col-xs-8").text
        info[header] = value

    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("----")

    article_content = soup.find("section", class_="article-content")

    info2 = {}
    for h2 in article_content.find_all("h2"):
        key = h2.text

        next_element = h2.find_next_sibling(["ul", "p"])

        if next_element.name == "ul":
            values = [li.text for li in next_element.find_all("li")]
            info2[key] = values
        else:
            info2[key] = next_element.text

    for key, value in info2.items():
        print(f"{key}:")
        if isinstance(value, list):
            for item in value:
                print(f" - {item}")
        else:
            print(f"  {value}")
        print()
    
    with open(f"{name}.txt", "w") as f:
        for key, value in info.items():
            f.write(f"{key}: {value}\n")
        f.write("----\n")
        for key, value in info2.items():
            f.write(f"{key}:\n")
            if isinstance(value, list):
                for item in value:
                    f.write(f" - {item}\n")
            else:
                f.write(f"  {value}\n")
            f.write("\n")

else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")