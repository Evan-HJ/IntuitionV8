from flask import *
import json
from datetime import datetime

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    
@app.route('/backup', methods=['GET'])
def backup():
    return render_template('backup home.html')

@app.route('/meetings', methods=['GET'])
def meetings():
    return render_template('meetings.html')

# @app.route('/profile/tutor/<string:usr>')  # Username
# def showTutorProfile(usr):  # DONE
#     usr_doc = dbscript.getTutorDoc({
#         'usrname': usr
#     })

#     return render_template('profile.html', usr_doc=usr_doc, type='tutor')


# @app.route('/profile/tutee/<string:usr>')  # Username
# def showTuteeProfile(usr):  # DONE
#     # NOTE: If usr not found, return home and flash
#     usr_doc = dbscript.getTuteeDoc({
#         'usrname': usr
#     })

#     if usr_doc:
#         return render_template('profile.html', usr_doc=usr_doc, type='tutee')
#     else:
#         flash("User not found", "error")
#         return redirect(url_for('home'))

if (__name__ == '__main__'):
    app.run(debug=True)
