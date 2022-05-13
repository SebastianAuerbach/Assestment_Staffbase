from PIL import Image
import requests
from bs4 import BeautifulSoup
import requests
import csv
import json

#get a new picture for every colleague
def newpic():
    r = requests.get("https://boredhumans.com/apes.php")
    content = r.content
    soup = BeautifulSoup(content, "html.parser")
    image = soup.findAll('img')[1]
    image = image["src"]
    return(image)

#get data from csv and "convert" it to json
with open("Assestment Staffbase\Example_Good.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    data = {"payloads": []}
    for row in reader:
        for att in row:
            arr = att.split(";")
            data["payloads"].append({"externalID": arr[0],
                                    "emails/primary": arr[3],
                                    "sendEmail": False,
                                    "avatar": newpic(),
                                    "lastName": arr[2],
                                    "firstName": arr[1],
                                    "position": arr[4],
                                    "department": arr[5]
            })

#write generated payload to .json just for debugging 
with open ("payloads.json", "w") as f:
    json.dump(data, f, indent=2)


url = "https://backend.staffbase.com/api/users"
headers = {
    'user-agent': "vscode-restclient",
    'authorization': "Basic TOKEN",
    'content-type': "application/json"
    }

#probably add some kind of logging, or at least write the response in a text file
for val in data["payloads"]:
    payload = val
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)




