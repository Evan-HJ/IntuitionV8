from flask import *
import dbscript
import json
from helper import *
from datetime import datetime
app = Flask(__name__, static_url_path='/static')
# static_url_path='',
# static_folder='LEGIT FINAL/static')
app.secret_key = 'secretkey'


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/tutee/login', methods=['GET'])
def tuteeLogin():  # DONE
    return render_template('tuteelogin.html')


@app.route('/tutee/login', methods=['POST'])
def checkLoginTutee():  # DONE
    # If success, go home, else flash and go /tutorlogin

    pwd = str(request.form.get('pwd'))
    usrname = str(request.form.get('usrname'))

    session['usr'] = dbscript.tuteeLogin(usrname, pwd)
    if (session.get('usr')):
        session['usr'] = str(session.get('usr'))

    if session.get('usr'):
        session['loggedin'] = True
        session['type'] = 'tutee'
        session['usrname'] = usrname
        flash('Logged in succesfully!', "success")
        return redirect(url_for('home'))
    else:
        session['loggedin'] = False
        flash('Wrong username or password', 'error')
        return redirect(url_for('tuteeLogin'))


@app.route('/tutor/login', methods=['GET'])
def tutorLogin():  # DONE
    return render_template('tutorlogin.html')


@app.route('/tutor/login', methods=['POST'])
def checkLoginTutor():  # DONE
    pwd = str(request.form.get('pwd'))
    usrname = str(request.form.get('usrname'))

    session['usr'] = dbscript.tutorLogin(usrname, pwd)
    if (session.get('usr')):
        session['usr'] = str(session.get('usr'))

    if session.get('usr'):
        session['loggedin'] = True
        session['type'] = 'tutor'
        session['usrname'] = usrname
        flash('Logged in succesfully!', "success")
        return redirect(url_for('home'))
    else:
        session['loggedin'] = False
        flash('Wrong username or password', 'error')
        return redirect(url_for('tutorLogin'))


@app.route('/tutor/signup', methods=['GET'])
def tutorSignup():  # DONE
    return render_template('tutorsignup.html')


@app.route('/tutor/signup', methods=['POST'])
def addTutor():  # DONE
    name = request.form.get('name')
    usrname = request.form.get('usrname')
    pwd = request.form.get('pwd')
    age = int(request.form.get('age'))
    school = request.form.get('school')

    result = dbscript.tutorAdd(name, usrname, age, school, pwd)
    if result:
        flash("Signed up successfully! You can now log in", 'success')
        return redirect(url_for('home'))
    else:
        flash('Username is taken', 'error')
        return redirect(url_for('tutorSignup'))


@app.route('/tutee/signup', methods=['GET'])
def tuteeSignup():  # DONE
    return render_template('tuteesignup.html')


@app.route('/tutee/signup', methods=['POST'])
def addTutee():  # DONE
    name = request.form.get('name')
    usrname = request.form.get('usrname')
    pwd = request.form.get('pwd')
    age = request.form.get('age')
    school = request.form.get('school')

    result = dbscript.tuteeAdd(name, usrname, age, school, pwd)
    if result:
        flash("Signed up successfully! You can now log in", 'success')
        return redirect(url_for('home'))
    else:
        flash('Username is taken', 'error')
        return redirect(url_for('tuteeSignup'))


@app.route('/profile/tutor/<string:usr>')  # Username
def showTutorProfile(usr):  # DONE
    usr_doc = dbscript.getTutorDoc({
        'usrname': usr
    })

    return render_template('profile.html', usr_doc=usr_doc, type='tutor')


@app.route('/profile/tutee/<string:usr>')  # Username
def showTuteeProfile(usr):  # DONE
    # NOTE: If usr not found, return home and flash
    usr_doc = dbscript.getTuteeDoc({
        'usrname': usr
    })

    if usr_doc:
        return render_template('profile.html', usr_doc=usr_doc, type='tutee')
    else:
        flash("User not found", "error")
        return redirect(url_for('home'))


@app.route('/myprofile')
def myprofile():
    if session.get('loggedin'):
        return redirect('/profile/{}/{}'.format(session.get('type'), session.get('usrname')))
    else:
        flash('Log in to view this page', 'error')
        return redirect(url_for('home'))


@app.route('/meetings')
def meetings():
    if not session.get('loggedin'):
        flash('Log in to view this page', 'error')
        return redirect(url_for('home'))

    if session.get('type') == 'tutor':
        usr_doc = dbscript.getTutorDoc({
            'usrname': session.get('usrname')
        })
        meetings = [dbscript.getMeeting({
            '_id': meetingID
        })for meetingID in usr_doc['meetings']]

        for i in range(len(meetings)):
            meetings[i]['tutorusrname'] = dbscript.getTutorDoc({'_id': ObjID(meetings[i]['tutorID'])})['usrname']

            meetings[i]['subject'] = meetings[i]['subject'].capitalize()

            if (session.get('type') == 'tutee'):
                meetings[i]['registered'] = (meetings[i]['_id'] in usr_doc['meetings'])
            else:
                meetings[i]['registered'] = False

        return render_template('meetings.html', usr_doc=usr_doc, meetings=meetings)
    elif session.get('type') == 'tutee':
        usr_doc = dbscript.getTuteeDoc({
            'usrname': session.get('usrname')
        })
        meetings = [dbscript.getMeeting({
            '_id': meetingID
        }) for meetingID in usr_doc['meetings']]

        for i in range(len(meetings)):
            meetings[i]['tutorusrname'] = dbscript.getTutorDoc({'_id': meetings[i]['tutorID']})['usrname']
            meetings[i]['subject'] = meetings[i]['subject'].capitalize()

            if (session.get('type') == 'tutee'):
                meetings[i]['registered'] = (meetings[i]['_id'] in usr_doc['meetings'])
            else:
                meetings[i]['registered'] = False
        return render_template('meetings.html', usr_doc=usr_doc, meetings=meetings)

# @app.route('/meetings/<string:id>')
# def viewmeeting(id):
#     meeting = dbscript.getMeeting({'_id': ObjID(id)})
#     meeting['start'] = meeting['start'].strftime("%m/%d/%Y, %H:%M:%S")
#     meeting['end'] = meeting['end'].strftime("%m/%d/%Y, %H:%M:%S")
#     tutor_doc = dbscript.getTutorDoc({'_id': meeting['tutorID']})
#     return render_template('viewmeeting.html', tutor_doc = tutor_doc, meeting_doc = meeting)


@app.route('/host', methods=['GET'])
def host():
    if not session.get('loggedin'):
        flash('Log in to view this page', 'error')
        return redirect(url_for('home'))

    if session.get('type') == 'tutee':
        flash('Log in as tutor to view this page', 'error')
        return redirect(url_for('home'))
    return render_template('createmeeting.html')


@app.route('/host', methods=['POST'])
def createmeeting():
    title = request.form.get('title')
    subject = request.form.get('subject')
    level = request.form.get('level')
    date = request.form.get('date')
    start = request.form.get('start')
    end = request.form.get('end')

    res = dbscript.addMeeting(title, subject, level, start, end, date, session.get('usr'))
    return redirect(url_for('meetings'))


@app.route('/register/<string:id>', methods=['GET'])
def register(id):
    if not session.get('loggedin'):
        flash('Log in to view this page', 'error')
        return redirect(url_for('home'))

    meetingDoc = dbscript.getMeeting({'_id': ObjID(id)})
    registered = (ObjID(session.get('usr')) in meetingDoc['tuteeID'])

    tutorDoc = dbscript.getTutorDoc({'_id': meetingDoc['tutorID']})
    tutorDoc.pop('pwd', None)

    tuteeDoc = [
        dbscript.getTuteeDoc({'_id': ObjID(tuteeID)})
    for tuteeID in meetingDoc['tuteeID']]

    return render_template('register.html', tuteeDoc = tuteeDoc, meetingDoc=meetingDoc, registered=registered, meetingID=id, tutorDoc=tutorDoc, usrtype=session.get('type'))


@app.route('/register/<string:id>', methods=['POST'])
def addRegister(id):
    dbscript.regForMeeting(session.get('usr'), id)
    return register(id)


@app.route('/search', methods=['GET', 'POST'])
def search():
    # NOTE: Displays randomly if no search

    if request.method == 'GET':
        meetings = dbscript.searchMeeting({})
        if session.get('type') == 'tutee':
            usr_doc = dbscript.getTuteeDoc({'_id': ObjID(session.get('usr'))})

        for i in range(len(meetings)):
            meetings[i]['tutorusrname'] = dbscript.getTutorDoc({'_id': meetings[i]['tutorID']})['usrname']
            meetings[i]['subject'] = meetings[i]['subject'].capitalize()

            if (session.get('type') == 'tutee'):
                meetings[i]['registered'] = (meetings[i]['_id'] in usr_doc['meetings'])
            else:
                meetings[i]['registered'] = False

        return render_template('searchresults.html',
                               subject="",
                               level="",
                               date=datetime.today(),
                               start=None,
                               end=None,
                               meetings=meetings
                               )
    elif request.method == 'POST':
        terms = ['subject', 'level', 'date']
        fields = {}
        for term in terms:
            if request.form.get(term):
                fields[term] = request.form.get(term)

        if request.form.get('start'):
            lower = {'start': request.form.get('start')}
        else:
            lower = {}

        if request.form.get('end'):
            upper = {'end': request.form.get('end')}
        else:
            upper = {}

        meetings = dbscript.searchMeeting(fields, upper, lower)
        if session.get('type') == 'tutee':
            usr_doc = dbscript.getTuteeDoc({'_id': ObjID(session.get('usr'))})

        for i in range(len(meetings)):
            meetings[i]['tutorusrname'] = dbscript.getTutorDoc({'_id': meetings[i]['tutorID']})['usrname']
            meetings[i]['subject'] = meetings[i]['subject'].capitalize()

            if (session.get('type') == 'tutee'):
                meetings[i]['registered'] = (meetings[i]['_id'] in usr_doc['meetings'])
            else:
                meetings[i]['registered'] = False
        return render_template('searchresults.html',
                               subject=request.form.get('subject'),
                               level=request.form.get('level'),
                               date=request.form.get('date'),
                               start=request.form.get('start'),
                               end=request.form.get('end'),
                               meetings=meetings
                               )


if (__name__ == '__main__'):
    app.run(debug=True)
