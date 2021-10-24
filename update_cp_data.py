import requests as r 
from bs4 import BeautifulSoup
import pandas as pd 

def cp_update():
    session = r.Session()
    s = session.get('https://clist.by/')

    soup = BeautifulSoup(s.content, 'html.parser')
    events = soup.find_all('div', class_='contest')
    data = {}
    category = []
    name = []
    date_time = []
    length = []
    link = []
    location = []
    type_ = []

    for event in events:
        ev = event.find('a', class_="data-ace")['data-ace']
        s = str(ev)
        s = s.split('"')
        category.append('Contest')
        name.append(s[3])
        date_time.append( s[17] +'( IST )' )

        st = pd.to_datetime(s[17])
        en = pd.to_datetime(s[21])
        length.append(en-st)
        link.append( s[7].split(' ')[1] )
        location.append('Everywhere, Worldwide'  )
        type_.append( 'Digital Only' )

    cp_data = {
        'Category':category, 
        'Name':name,  
        'Date/Time':date_time, 
        'Length':length, 
        'Link':link, 
        'Location':location, 
        'Type':type_
    }

    df_cp = pd.DataFrame(cp_data)
    df_cp.to_csv('data_cp.csv', mode='w', index=False)

    return 'Data Updated'