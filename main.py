from flask import Flask, render_template
import requests 

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
