from bs4 import BeautifulSoup
import requests 
import re
from pathlib import Path

def startSession(pinNumber, StudentlastName): 
    URL = "http://orders.flashphotography.com/Orders/" 
    payload = { 
        "PIN": pinNumber, 
        "LastName": StudentlastName,
        "btnContinuePIN": "Continue >>"
    } 
    session = requests.session() 
    response = session.post(URL, data=payload)
    if (response.status_code == 200):
        return response
    else:
        return 'Error'

def imageGrabber(userID,lastName,id,fs,s):
    for f in range(len(fs)):
        if f == 0:
            initURL = f"http://magnifier.flashphotography.com/Magnify.aspx?O={id}&R={fs[f]}&F={s[0]}&A=71994"
            magURL = f"http://magnifier.flashphotography.com/Thumbnails/{id}/{fs[f]}/{s[0]}.jpg"
        else:
            initURL = f"http://magnifier.flashphotography.com/Magnify.aspx?O={id}&R={fs[f]}&F={s[1]}&A=71994"
            magURL = f"http://magnifier.flashphotography.com/Thumbnails/{id}/{fs[f]}/{s[1]}.jpg"
        
        requests.get(initURL)
        img_data = requests.get(magURL).content
        path = f'/var/www/html/ffp/images/{userID}/{lastName}'
        Path(path).mkdir(parents=True, exist_ok=True)
            
        # with open(f'{path}/image_{fs[f]}{s[1]}.jpg', 'wb') as handler:
        with open(f'{path}/image_{f}.jpg', 'wb') as handler:
            handler.write(img_data)
            print(f'Downloaded image {f}')
    return path

def verify(response, lastName):
    soup = BeautifulSoup(response.content, "html.parser") 
    lastNameVerification = soup.find(attrs={"id": "labGraduate"}).text.split(' ')
    if(lastName.upper() == lastNameVerification[-1].upper()):
        print(f'Logged in as \'{lastNameVerification}\'')
        return True
    else:
        return False

def getId(response):
    id = ""
    soup = BeautifulSoup(response.content, "html.parser") 
    ImagesFromHTML = soup.findAll(attrs={"class": "Proof"}) 
    for link in ImagesFromHTML:
        if id == "":
            id = link.get('src').rsplit("/",-1)[4]
    return id

def getS(response,):
    s = []
    soup = BeautifulSoup(response.content, "html.parser") 
    ImagesFromHTML = soup.findAll(attrs={"class": "Proof"}) 
    for link in ImagesFromHTML:
        s.append(link.get('src').rsplit("/",-1)[-1].strip("t.jpg"))
    return s

def getF(response,):
    f = []
    soup = BeautifulSoup(response.content, "html.parser") 
    ImagesFromHTML = soup.findAll(attrs={"class": "Proof"}) 
    for link in ImagesFromHTML:
        f.append(link.get('src').rsplit("/",-1)[5])
    return f
    
def run(idInput, lastNameInput):
    print("""

  __ _           _           _           _                              _           
 / _| |         | |         | |         | |                            | |          
| |_| | __ _ ___| |__  _ __ | |__   ___ | |_ ___   __ _ _ __ __ _ _ __ | |__  _   _ 
|  _| |/ _` / __| '_ \| '_ \| '_ \ / _ \| __/ _ \ / _` | '__/ _` | '_ \| '_ \| | | |
| | | | (_| \__ \ | | | |_) | | | | (_) | || (_) | (_| | | | (_| | |_) | | | | |_| |
|_| |_|\__,_|___/_| |_| .__/|_| |_|\___/ \__\___/ \__, |_|  \__,_| .__/|_| |_|\__, |
                      | |                          __/ |         | |           __/ |
                      |_|                         |___/          |_|          |___/ 
                      
                        By Fowzy, Github.com/fowzy
""")
    # idInput=int(input('Enter ID: '))
    # lastNameInput=str(input('Enter Last Name: '))
    response = startSession(idInput, lastNameInput)
    if(verify(response, lastNameInput) == True):
        print('Verified...')
        selfId = getId(response)
        selfF = getF(response)
        selfS = getS(response)
        path = imageGrabber(idInput, lastNameInput, selfId,selfF,selfS)
        return path
    else:
        print('Wrong ID or Last Name. Can\'t verify, please try again!')
    
# if __name__ == "__main__":
#     main()