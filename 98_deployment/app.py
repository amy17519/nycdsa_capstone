from flask import Flask, render_template, redirect, request, url_for
import pandas as pd
from scripts.Supervisor import *
# from flask_googlemaps import GoogleMaps,Map

user_ids = pd.read_csv('user_id.csv')

app = Flask(__name__)

@app.route("/")
def login():
    if request.method == 'POST':
        user1 = request.form['user1']
        user2 = request.form['user2']
        return redirect(url_for('mapview'), user1=user1, user2=user2)
    else:
        return render_template('login.html')


@app.route('/mapview', methods=['POST'])
def mapview():
    user1 = request.form['user1']
    user2 = request.form['user2']
    return render_template('example.html', user1=user1, user2=user2)

@app.route('/model', methods=['GET','POST'])
def getResult():
    user1_row_num = int(request.form.get('user1'))
    user2_row_num = int(request.form.get('user2'))
    user1_id =  user_ids['user_id'][user1_row_num]
    user2_id = user_ids['user_id'][user2_row_num]
    user_id = [user1_id, user2_id]
    print 'here'

    sw_latitude = request.form.get('sw_latitude')
    sw_longitude = request.form.get('sw_longitude')
    ne_latitude = request.form.get('ne_latitude')
    ne_longitude = request.form.get('ne_longitude')
    bounding_box = {
         'sw_latitude': sw_latitude,
         'sw_longitude': sw_longitude,
         'ne_latitude': ne_latitude,
         'ne_longitude': ne_longitude
     }


    search_params = {
        "terms" : "restaurant,japanese,chinese",
        "lang": "en"
     }

    result = supervisor(user_id,40,bounding_box,search_params)
    print type(result)
    return "success"


if __name__ == "__main__":
    app.run(
        debug=True
    )