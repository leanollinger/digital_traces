# This is an application using deta for my digital traces classes

The main goal of this application is to learn more about cookies and logs using deta and flask. 
You can see my website here : **https://sf4h7q.deta.dev/**

## Main features

- See the welcome page : just go to the website
- See predefined logs : add **/logs** to url 
- See your logs : add **/textbox** to url
- See cookies : add **/cookie** to url 
- Go to Google Analytics : add **/cookieganalytics** to url. You will need to login to google to access it. 
- See the number of visitor of the website : add **/visitor** to url.
- See the trend between cat and dog : add **/trend** to url. 

You will also see a notebook that contains the timer log part. 

## Requirements to run the application 

flask 
requests 
google-api-python-client  
oauth2client  
python-dotenv  
pytrends

## Main command : 

**Log into deta**
```sh
deta login
```

**Deploy your application**
```sh
deta deploy
```
