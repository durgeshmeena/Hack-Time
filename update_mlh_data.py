import requests as r 
from bs4 import BeautifulSoup
import pandas as pd 

def mlh_update():
    session = r.Session()
    s = session.get('https://mlh.io/seasons/2022/events')

    soup = BeautifulSoup(s.content, 'html.parser')
    events = soup.find_all('div', class_='event')
    data = {}
    category = []
    name = []
    date_time = []
    length = []
    link = []
    image = []
    location = []
    type_ = []

    for event in events:
        place_type = event.find_all('span')
        category.append('MLH')
        name.append(event.find('h3', class_="event-name").text)
        date_time.append( event.find('p', class_="event-date").text+'( EST )' )
        date = event.find_all('meta')
        s = pd.to_datetime(date[0]['content'], yearfirst=True)
        e = pd.to_datetime(date[1]['content'], yearfirst=True)
        length.append(e-s)
        link.append( event.find('a')['href'] )
        image.append( event.find('img')['src'] )
        location.append( place_type[0].text+', '+place_type[1].text )
        type_.append( place_type[2].text )

    mlh_data = {
        'Category':category, 
        'Name':name,  
        'Date/Time':date_time, 
        'Length':length, 
        'Link':link, 
        'Image':image, 
        'Location':location, 
        'Type':type_
    }

    df_mlh = pd.DataFrame(mlh_data)
    df_mlh.to_csv('data_mlh.csv', mode='w', index=False)

    return 'Data Updated'