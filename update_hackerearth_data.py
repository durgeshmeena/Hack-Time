import requests as r 
from bs4 import BeautifulSoup
import pandas as pd 

def hackerearth_update():
    session = r.Session()
    s = session.get('https://www.hackerearth.com/challenges/')


    soup = BeautifulSoup(s.content, 'html.parser')
    events = soup.find_all('div', class_='challenge-card-modern')
    category = []
    name = []
    challenge = []
    status = []
    link = []
    image = []
    company = []
    registration = []


    for event in events:
        if event.find('div' , class_='company-details') and event.find('div', class_="event-image"):
            category.append('Hackathons')
            name.append(event.find('span', class_="challenge-list-title").text)
            challenge.append(event.find('div', class_="challenge-type").text.split('\n')[2].split(' ')[-1])
            if event.find_all('div', class_="caps")[1].text =="ENDS IN":
                status.append('Live')
            else:
                status.append(event.find('div', class_='date').text)    

            company.append( ' '.join(event.find('div' , class_='company-details').text.split('\n')[1].split(' ')[1:]) )
            regs = event.find('div', class_="registrations").text.split('\n')[1]
            if regs and regs[0]== '':
                regs = regs.split(' ')[1]
            registration.append(regs)
            lnk = event.find('a', class_="challenge-card-link")['href']
            if 'http' not in lnk:
                lnk = 'https://www.hackerearth.com'+lnk
            link.append( lnk )
            image.append( event.find('div', class_="event-image")['style'].split("'")[1] )



    hackerearth_data = {
        'Category':category, 
        'Name':name,  
        'Type':challenge, 
        'Status':status, 
        'Company':company, 
        'Registrations/Prize':registration, 
        'Link':link, 
        'image':image
    }

    df_hackerearth = pd.DataFrame(hackerearth_data)
    df_hackerearth.to_csv('data_hackerearth.csv', mode='w', index=False)

    return 'Data Updated'