from flask import Flask, render_template, g, redirect, request, jsonify
#from flask_googlemaps import GoogleMaps
#from flask_googlemaps import Map
#import requests

app = Flask(__name__)
#GoogleMaps(app)

@app.route("/")
def login():
    if request.method == 'POST':
        user1=request.form['user1']
        user2=request.form['user2']
        return redirect(url_for('mapview'),user1=user1,user2=user2)
    else:
        return render_template('login.html')

@app.route('/mapview', methods=['POST'])
def mapview():
    user1=request.form['user1']
    user2 = request.form['user2']
    return render_template('example.html',user1=user1,user2=user2)

#@app.route('recommend', methods=['GET'])
#def getRecommend():
#    result = request


if __name__ == "__main__":
    app.run(debug=True)
