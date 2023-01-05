from flask import Flask, render_template
import requests 
from pytrends.request import TrendReq
import os
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'digitalsource.json'

VIEW_ID = "281211325" # str(os.getenv("View_ID")) # Get from env

app = Flask(__name__)

@app.route('/', methods=["GET"])

def hello_world():
    prefix_google = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-250912185-1"></script> <script>
window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date());
gtag('config', 'UA-250912185-1'); </script>
"""
    
    return prefix_google+"Hello Word"

@app.route('/logs', methods=["GET"])
def log():
    return render_template("logs.html")+"Let's see on your console"

@app.route('/textbox')
def textlog():
    return "Write something"+render_template("textbox.html")+"Let's see on your console after you submit to see what happened"


@app.route('/cookie', methods=["GET","POST"])
def mycookies():
    req = requests.get("https://www.google.com/")
    return req.cookies.get_dict() 

@app.route('/cookieganalytics', methods=["GET","POST"])
def mycookieganalytics():
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a250912185w345031321p281211325")
    return req.text


@app.route('/visitor', methods = ['GET', 'POST'])
def get_nb_visitors():

    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    nb_visitor = print_response(response)
    return "Number of visitors : " + str(nb_visitor) 


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics

def get_report(analytics):
    return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': []
          #'dimensions': [{'name': 'ga:country'}]
        }]
      }
  ).execute()

def print_response(response):
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        
        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])
            
            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ', dimension)
                
            for i, values in enumerate(dateRangeValues):
                print('Date range:', str(i))
                
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    visitors = value
    return str(visitors)

@app.route('/trend', methods=["GET","POST"])
def googletrendchart():
    topic_1 = "Chien"
    topic_2 = "Chat"
    pytrends = TrendReq()
    pytrends.build_payload(kw_list=[topic_1, topic_2], timeframe='today 5-y', geo='FR')
    df = pytrends.interest_over_time()
    
    data_topic_1 = df[topic_1].tolist()
    data_topic_2 = df[topic_2].tolist()
    data_date = df.index.values.tolist()
    
    timestamp_in_seconds=[element/1e9 for element in data_date]
    date= [datetime.fromtimestamp(element) for element in timestamp_in_seconds]
    days=[element.date() for element in date]
    months=[element.isoformat() for element in days]
    params = {
        "type": 'line',
        "data": {
            "labels": months,
            "datasets": [{
                "label": topic_1,
                "data": data_topic_1,
                "borderColor": '#3e95cd',
                "fill": 'false',
            },
            {
                "label": topic_2,
                "data": data_topic_2,
                "borderColor": '#ffce56',
                "fill": 'false',
            }
            ]
        },
        "options": {
            "title": {
                "text": 'Comparaison entre'# + str(topic_1) + " et " + str(topic_2)
            },
            "scales": {
                "yAxes": [{
                     "ticks": {
                        "beginAtZero": 'true'
                    }
                }]
            }
        }
    }
                                        
    prefix_chartjs = """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
         <canvas id="myChart" width="1200px" height="700px"></canvas>""" + f"""
        <script>
        var ctx = document.getElementById('myChart');
        var myChart = new Chart(ctx, {params});
        </script>

        """
  
    return prefix_chartjs