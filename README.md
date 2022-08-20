# **HackThisFall2.0-LightDev**


 ## Build a WhatsApp Chatbot With Python, Flask and Twilio
A chatbot is a software application that is able to conduct a conversation with a human user.
Hack-Time, chatbot which gives details about upcoming/running Hackathons and CP contests. 
Build using the Twilio API for WhatsApp and the Flask framework for Python.

 ### Requirements
  >[Python](https://python.org/) <br>
  >[Flask](https://www.palletsprojects.com/p/flask/) <br>
  >[ngrok](https://ngrok.com/) <br>
  >[Twilio account](https://www.twilio.com/console/)

  <br><br>

  ### [Configure the Twilio WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
  
  Twilio provides a WhatsApp sandbox where you can easily develop and test your application.
  Connect your smartphone to the sandbox. 
  **Twilio Console -> Messaging -> Try it Out -> Send a WhatsApp message** <br>
  The WhatsApp sandbox page will show you the sandbox number assigned to your account, and a join code.

  ### [Configure the ngrok](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbo)
  To make local host server service reachable from the Internet we can use ngrok which allocate a temporary public URL that redirects HTTP requests to our local host server         where,  we can handle request and send back suitable Response to Whatsapp <br>
  **Twilio Console -> Messaging -> Setting -> WhatsApp sandbox setting** <br>
  and paste ngrok url in **WHEN A MESSAGE COMES IN** field <br>
  <img src="https://user-images.githubusercontent.com/58581435/136695017-1bf41505-36f6-4d8b-ae26-896489e1e243.png" width="500px" /> 
  <img src="https://user-images.githubusercontent.com/58581435/136695143-9a82b28c-6faa-496f-931c-26f1befc038d.png" width="400px"/> <br>
  
  In our case we are handling POST request at http://localhost:5000/bot and our ngrok url is https://24df-2401-4900-36a4-a53b-1068-c2c9-b470-8e64.ngrok.io so our final url      will be https://24df-2401-4900-36a4-a53b-1068-c2c9-b470-8e64.ngrok.io/bot


  <br><br>
  ## Chat
  ![image](https://user-images.githubusercontent.com/58581435/185737207-281dd4e2-610d-4013-81b2-25c45c7133bb.png)
  
  
  ## Developed by
  
  ### [Durgesh Kumar Meena](https://github.com/durgeshmeena/) <br>
  ### [Monu Kumar](https://github.com/MonuKumar1)
  
  
