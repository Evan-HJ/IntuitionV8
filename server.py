from flask import *
import json
from datetime import datetime
from json_handler import JsonHandler
app = Flask(__name__, static_url_path='/static')

json_handler = JsonHandler('events.json', 'profiles.json')
all_tags = ["Chemistry", "Hackathon",  "Math", "Economics", "Physics"]

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    
@app.route('/backup', methods=['GET'])
def backup():
    return render_template('backup home.html')

@app.route('/meetings', methods=['GET'])
def meetings():
    return render_template('meetings.html')

@app.route('/search_profiles', methods=['GET', 'POST'])
def search_profiles():
    if request.method == 'POST':
        search_terms = request.form.to_dict()
        search_dict = {}
        for key, value in search_terms.items():
            if key.startswith('tag/'):
                if value == 'on':
                    if 'tags' not in search_dict:
                        search_dict['tags'] = [] 
                    search_dict['tags'].append(key[4:])
            elif value:
                search_dict[key] = value

        result = json_handler.search_profiles(search_dict=search_dict)
        print('SEARCH TERMS: ', search_dict)
        print('RESULT: ', result)
    
        return render_template('search_profiles.html', tags = all_tags, search_dict = search_dict, profiles = result)
    else:
        return render_template('search_profiles.html', tags = all_tags)


@app.route('/search_events', methods=['GET', 'POST'])
def search_events():
    if request.method == 'POST':
        search_terms = request.form.to_dict()
        search_dict = {}
        for key, value in search_terms.items():
            if key.startswith('tag/'):
                if value == 'on':
                    if 'tags' not in search_dict:
                        search_dict['tags'] = [] 
                    search_dict['tags'].append(key[4:])
            elif value:
                search_dict[key] = value

        result = json_handler.search_events(search_dict=search_dict)
        print('SEARCH TERMS: ', search_dict)
        print('RESULT: ', result)
    
        return render_template('search_events.html', tags = all_tags, search_dict = search_dict, events = result)
    else:
        return render_template('search_events.html', tags = all_tags)


@app.route('/profile/<string:name>')  # Username
def showProfile(name):  # DONE
    profile = json_handler.get_profile_by_name(name)

    return render_template('profile.html', profile=profile)


@app.route('/event/<string:name>')  # Username
def showEvent(name):  # DONE
    event = json_handler.get_event_by_name(name)

    return render_template('event.html', event=event)

if (__name__ == '__main__'):
    app.run(debug=True)
