from typing import Tuple
from flask import Flask, request
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import json
from decouple import config
import asyncio

from bs4 import BeautifulSoup
import regex as re 
import numpy as np
import pandas as pd 

from update_mlh_data import mlh_update
from update_cp_data import cp_update
from update_hackerearth_data import hackerearth_update
app = Flask(__name__)
app.secret_key = config('APP_SECRET')

session = {'Login':False, 'State':0, 'Loaded':True, 'Catagory':None, 'Stage':0}

@app.route('/')
def index():
    return "Server Started"

def write(data):
    session['Loaded'] = True
    with open("data.json", "w") as database:
        json.dump(data, database) 

def go():
    data = '' # get_user(config('USER'), config('PASSWORD'))
    return  write(data)     


@app.route( '/bot', methods=['POST']) 
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    # handling session 
            # msg.body('Choose one of the following to get imformation\n*1.* *MLH*- MLH Hackathons \n*2* *CP*- Contest \n*i.* *Hacks*- Hackathons \n*4.* *Close*- to end your session. \n*5.* *UpdateMLH*- To refresh mlh hachathons data.  \n*6.* *UpdateCP*- To refresh cp contest data. \n*7.* *UpdateHacks*- To refresh hachathons data. \n*8*  *Home*- Go back to home')


    if session['Login']:
        if '?' in incoming_msg:
            if session['Loaded']:
                msg.body('Choose one of the following to get imformation\n*1.* *Hackathon*- for Hackathons \n*2* *CP*- Contest')
                responded = True  
            else:
                msg.body('still Loading!. Please wait for few seconds')
                responded = True 

        if not session['Loaded']: 

            if 'mlh' or 'cp' or 'hacks' or 'updatemlh' or 'updatecp' or 'updatehacks' in incoming_msg:
                msg.body("*Loading data*\nthis may take some time. Please reply with *?* to know status of your information")
                responded = True
    

            elif 'logout' in incoming_msg:
                session['Login'] = False
                with open("data.json", "w") as database:
                    json.dump({}, database) 
                msg.body('session ended sucessfully! \n*Thank you*')
                responded = True
            else:
                msg.body('your session alredy started. \n type *?* to know more.')     
                responded = True
                
   
        if session['Loaded']:
            if 'hackathon' in incoming_msg:
            
                msg.body('choose from following plateform \n1. *M*- MLH \n2. *H*- Hackerearth \n')
                responded = True

            elif 'cp' in incoming_msg:
                df = pd.read_csv('data_cp.csv')
                session['Catagory'] = 'CP'
                session['Stage'] = 
                while i<session['Stage']:
                    msg.body('Category: '+ '*'+ df.iloc[i, :]['Category'] +'*'+'\n' +'Name: ' + '*'+df.iloc[i, :]['Name']  +'*'+'\n' +      'Date/Time: ' +'*'+df.iloc[i, :]['Date/Time']   +'*'+'\n' + 'Length: ' +'*'+df.iloc[i, :]['Length']     +'*'+'\n' +  'Link: '+   '*'+df.iloc[i, :]['Link']      +'*'+'\n' +  'Location: ' + '*'+df.iloc[i, :]['Location'] +'*'+'\n' +       'Type: ' + '*'+df.iloc[i, :]['Type']  + '*'+'\n'  )
                responded = True

            elif 'home' in incoming_msg:
                
                responded = True

            elif 'logout' in incoming_msg:
                session['Login'] = False
                msg.body('session ended sucessfully! \n*Thank you*')
                responded = True


            else:
                msg.body('Type *?* to know your command')     
                responded = True
            if not responded:
                msg.body('an Error occured! again Type *START* to start bot')  
         
    
    else:
        if "show" in incoming_msg:
            session['Login'] = True
            msg.body('Choose one of the following to get imformation\n*1.* *Hackathon*- for Hackathons \n*2* *CP*- Contest')
            responded = True 
        else:
            msg.body('*Welcome user* \nwe are one step solution for all hackathons and contest \ntype *Show* to show available options')
            responded = True             

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
