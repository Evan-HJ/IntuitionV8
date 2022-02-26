from flask import *
import json
from datetime import datetime

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

    
@app.route('/meetings', methods=['GET'])
def meetings():
    return render_template('meetings.html')

if (__name__ == '__main__'):
    app.run(debug=True)
