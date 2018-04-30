from flask import Flask, render_template, request
import requests
import json
import urllib
import pandas as pd
import StringIO
import base64
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize

app = Flask(__name__)

@app.route('/temperature', methods=['POST'])
def temperature():
    city = request.form['city']
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+',us&appid=c7b2a4a5393fc79135ab480ba2a256cb')
    json_object = r.json()
    k_temp = float(json_object['main']['temp'])
    f_temp = (k_temp - 273.15) * 1.8 + 32
    icon_id = str(json_object['weather'][0]['icon'])
    icon_url = 'http://openweathermap.org/img/w/'+icon_id+'.png'
    #Please replace this directory to the proper app/static folder for grading purposes, e.g "C:\Users\.....\project\static\icon.png"
    urllib.urlretrieve(icon_url, "C:\Users\Thinkpad\Desktop\Python Lectures\starter_file\static\icon.png")
    r2 = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+',us&appid=c7b2a4a5393fc79135ab480ba2a256cb')
    data = pd.json.loads(r2.text)
    df = json_normalize(data['list'])
    df['dt_txt'] = pd.to_datetime(df['dt_txt'])
    df['dt_txt'] = df['dt_txt'].dt.normalize()
    days = df['dt_txt'].unique()
    avg_temps = []
    dates = []
    for day in days:
        d = df.loc[df['dt_txt'] == day]
        temp_f = (d['main.temp'].mean() - 273.15) * 1.8 + 32
        avg_temps.append(temp_f)
    
    for day in days:
        ts = pd.to_datetime(str(day)) 
        d = ts.strftime('%Y.%m.%d')
        dates.append(d)
   
    img = StringIO.StringIO()
    y = avg_temps
    x = dates

    fig = plt.figure()
    fig.suptitle('5 day forecast')
    plt.plot(x,y,'bo')
    plt.xlabel('Dates')
    plt.ylabel('Mean Temperature (F)')
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue())
    return render_template('temperature.html', city=city, temp=f_temp, plot_url=plot_url)
            
@app.route('/')
def index():
    return render_template('index.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500
	
if __name__ == '__main__':
  app.debug = True	
  app.run(port=33507)

