import re
from typing import Tuple
from flask import Flask, request, make_response
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import json
from decouple import config

import pandas as pd 

from update_mlh_data import mlh_update
from update_cp_data import cp_update
from update_hackerearth_data import hackerearth_update
app = Flask(__name__)
app.secret_key = config('APP_SECRET')

session = {'Login':False, 'Loaded':True, 'Catagory':None, 'Stage':0}

@app.route('/')
def index():
    return "Server Started" 

@app.route( '/bot', methods=['POST']) 
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()

    # response.message('This is message 1 of 2.')
    # response.message('This is message 2 of 2.')
    # print(response)
    # return str(response)
    # msg = resp.message()
    # responded = True

    # handling session 
            # response.message('Choose one of the following to get imformation\n*1.* *MLH*- MLH Hackathons \n*2* *CP*- Contest \n*i.* *Hacks*- Hackathons \n*4.* *Close*- to end your session. \n*5.* *UpdateMLH*- To refresh mlh hachathons data.  \n*6.* *UpdateCP*- To refresh cp contest data. \n*7.* *UpdateHacks*- To refresh hachathons data. \n*8*  *Home*- Go back to home')


    if session['Login']:
        if '?' in incoming_msg:
            if session['Loaded']:
                response.message('Choose one of the following to get imformation\n*1.* *Hackathon*- for Hackathons \n*2* *CP*- Contest')
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
                with open("data.json", "w") as database:
                    json.dump({}, database) 
                response.message('session ended sucessfully! \n*Thank you*')
                responded = True
            else:
                response.message('your session alredy started. \n type *?* to know more.')     
                responded = True
                
   
        if session['Loaded']:
            if 'hack' in incoming_msg:
                df = pd.read_csv('data_hackerearth.csv')
                session['Catagory'] = 'Hacks'
                # session['Stage'] 
                i = session['Stage']
                session['Stage']=session['Stage']+5
                print('i=',i, ' --- ', 'new stage= ', session['Stage'])
                while i<session['Stage']:
                    response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Status: ' +'*'+df.iloc[i, :]['Status']   +'*'+'\n' + 'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n' + 'Company: ' + '*'+df.iloc[i, :]['Company']  + '*'+'\n'+ 'Registrations: ' + '*'+  str( df.iloc[i, :]['Registration'] ) + '*'+'\n'  )
                    response.media(df.iloc[i,:]['image'])
                    i+=1
                responded = True           
              

            elif 'cp' in incoming_msg:
                df = pd.read_csv('data_cp.csv')
                session['Catagory'] = 'CP'
                # session['Stage'] 
                i = session['Stage']
                session['Stage']=session['Stage']+5
                print('i=',i, ' --- ', 'new stage= ', session['Stage'])
                while i<session['Stage']:
                    response.message('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                    i+=1
                responded = True

            elif 'home' in incoming_msg:
                
                responded = True

            elif 'logout' in incoming_msg:
                session['Login'] = False
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
            response.message('Choose one of the following to get imformation\n*1.* *Hackathon*- for Hackathons \n*2* *CP*- Contest')
            responded = True 
        else:
            response.message('*Welcome user* \nwe are one step solution for all hackathons and contest \ntype *Show* to show available options')
            responded = True             

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
