from flask import Flask, render_template, redirect, request, jsonify
import requests
from model import *
# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map
# import requests
from flask import url_for

app = Flask(__name__)


# GoogleMaps(app)

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
    user1 = request.form.get('user1')
    user2 = request.form.get('user2')
    # print 'here'
    # print user2

    sw_latitude = request.form.get('sw_latitude')
    sw_longitude = request.form.get('sw_longitude')
    ne_latitude = request.form.get('ne_latitude')
    ne_longitude = request.form.get('ne_longitude')
    checkbox1 = request.form.get('checkbox1')
    bounding_box = {
        'sw_latitude': sw_latitude,
        'sw_longitude': sw_longitude,
        'ne_latitude': ne_latitude,
        'ne_longitude': ne_longitude
    }
    user_id = {
        "user1": user1,
        "user2": user2,
    }
    search_param = {

    }
    # result = supervisor(user_id,bounding_box,search_param)
    return str(checkbox1)




if __name__ == "__main__":
    app.run(
        debug=True
    )