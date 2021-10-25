import re
from typing import Tuple
from flask import Flask, request, session
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import json
from decouple import config

import pandas as pd 

from update_mlh_data import mlh_update
from update_cp_data import cp_update
from update_hackerearth_data import hackerearth_update
app = Flask(__name__)
app.secret_key = config('APP_SECRET')


@app.route('/')
def index():
    return "Server Started" 

@app.route( '/bot', methods=['POST']) 
def bot():
    session["Start"] = True
    # session = {'Login':False, 'Loaded':True, 'Catagory':None, 'Stage':0, 'CP':{ 'Catagory':False, 'Stage':0 }, 'MLH':{ 'Catagory':False, 'Stage':0 }, 'Hack':{ 'Catagory':False, 'Stage':0 }, }
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()

    if session['Login']:
        if '?' in incoming_msg:
            if session['Loaded']:
                response.message('\n*1.* *Hackathon*- for Hackathons \n*2.* *CP*- Contest \n *3.* *Home*- for home \n *4.* *Logout*- for ending session \n *5.* *UpdateM*- for refreshing MLH events data \n *6.* *UpdateC*- for refreshing Contest events data \n *7.* *UpdateO*- for refreshing Other Hackathons events data \n *8.* *Next*- to load more next data')
                responded = True  
            else:
                response.message('still Loading!. Please wait for few seconds')
                responded = True 

        if not session['Loaded']: 

            if 'mlh' or 'cp' or 'hacks' or 'updatemlh' or 'updatecp' or 'updatehacks' in incoming_msg:
                response.message("*Loading data*\nthis may take some time. Please reply with *?* to know status of your information")
                responded = True
    

            elif 'logout' in incoming_msg:
                session['Login'] = False
                session['Catagory'] = None
                session['CP']['Stage'] = session['Hack']['Stage'] = session['MLH']['Stage'] = 0 
                response.message('session ended sucessfully! \n*Thank you*')
                responded = True
            else:
                response.message('your session alredy started. \n type *?* to know more.')     
                responded = True
                
   
        if session['Loaded']:
            if 'hackathon' in incoming_msg:
                response.message('Choose one of the following to get imformation\n*1.* *MLH*- for Mlh Hackathons \n*2.* *Other*- for Other Hackathons')
                responded = True

            elif 'other' in incoming_msg:
                session['Catagory'] = 'Hack'
                df = pd.read_csv('data_hackerearth.csv')
                i = session['Hack']['Stage'] = 0
                session['Hack']['Stage'] = session['Hack']['Stage']+5
                # print('i=',i, ' --- ', 'new stage= ', session['Stage'])
                while i<session['Hack']['Stage']:
                    msg = response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Status: ' +'*'+df.iloc[i, :]['Status']   +'*'+'\n' + 'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n' + 'Company: ' + '*'+df.iloc[i, :]['Company']  + '*'+'\n'+ 'Registrations/Prize: ' + '*'+  str( df.iloc[i, :]['Registrations/Prize'] ) + '*'+'\n'  )
                    msg.media(df.iloc[i,:]['image'])
                    i+=1
                response.message('type *Next* to load more...') 
                responded = True     

            elif 'mlh' in incoming_msg:
                session['Catagory'] = 'MLH'
                df = pd.read_csv('data_mlh.csv')
                i = session['MLH']['Stage'] = 0
                session['MLH']['Stage'] = session['MLH']['Stage']+5
                # print('i=',i, ' --- ', 'new stage= ', session['Stage'])
                while i<session['MLH']['Stage']:
                    msg = response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                    msg.media(df.iloc[i,:]['Image'])
                    i+=1
                response.message('type *Next* to load more...') 
                responded = True                         
              

            elif 'cp' in incoming_msg:
                session['Catagory'] = 'CP'
                df = pd.read_csv('data_cp.csv')
                i = session['CP']['Stage'] = 0
                session['CP']['Stage'] = session['CP']['Stage']+5
                # print('i=',i, ' --- ', 'new stage= ', session['Stage'])
                while i<session['CP']['Stage']:
                    response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                    i+=1
                response.message('type *Next* to load more...') 
                responded = True

            elif 'next' in incoming_msg:
                       
                if session['Catagory'] == 'CP':
                    df = pd.read_csv('data_cp.csv')
                    i = session['CP']['Stage']
                    session['CP']['Stage'] = session['CP']['Stage']+5
                    while i<session['CP']['Stage']:
                        response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                        i+=1

                elif session['Catagory'] == 'Hack':
                    df = pd.read_csv('data_hackerearth.csv')
                    i = session['Hack']['Stage'] 
                    session['Hack']['Stage'] = session['Hack']['Stage']+5
                    while i<session['Hack']['Stage']:
                        msg = response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Status: ' +'*'+df.iloc[i, :]['Status']   +'*'+'\n' + 'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n' + 'Company: ' + '*'+df.iloc[i, :]['Company']  + '*'+'\n'+ 'Registrations/Prize: ' + '*'+  str( df.iloc[i, :]['Registrations/Prize'] ) + '*'+'\n'  )
                        msg.media(df.iloc[i,:]['image'])
                        i+=1

                elif session['Catagory'] == 'MLH':
                    df = pd.read_csv('data_mlh.csv')
                    i = session['MLH']['Stage']
                    session['MLH']['Stage'] = session['MLH']['Stage']+5
                    while i<session['MLH']['Stage']:
                        msg = response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                        msg.media(df.iloc[i,:]['Image'])
                        i+=1
                response.message('type *Next* to load more...') 
                responded = True

            elif 'updatem' in incoming_msg:
                mlh_update()
                response.message('Updating Data!!')
                responded = True    

            elif 'updateo' in incoming_msg:
                hackerearth_update()
                response.message('Updating Data!!')
                responded = True    

            elif 'updatec' in incoming_msg:
                cp_update()
                response.message('Updating Data!!')
                responded = True                    

            elif 'home' in incoming_msg:
                response.message('Choose one of the following to get imformation\n*1.* *Hackathon*- for Hackathons \n*2* *CP*- Contest')
                responded = True

            elif 'logout' in incoming_msg:
                session['Login'] = False
                session['Catagory'] = None
                session['CP']['Stage'] = session['Hack']['Stage'] = session['MLH']['Stage'] = 0 
                response.message('session ended sucessfully! \n*Thank you*')
                responded = True


            else:
                response.message('Type *?* to know your command')     
                responded = True
            if not responded:
                response.message('an Error occured! again Type *START* to start bot')  
         
    
    else:
        if "show" in incoming_msg:
            session['Login'] = True
            response.message('Choose one of the following to get imformation\n*1.* *Hackathon*- for Hackathons \n*2* *CP*- Contest \n \n *?*- for other commands')
            responded = True 
        else:
            response.message('*Welcome user* \nwe are one step solution for all hackathons and contest \ntype *Show* to show available options')
            responded = True             

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
