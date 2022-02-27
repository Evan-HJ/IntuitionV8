from flask import *
import json
from datetime import datetime
from json_handler import JsonHandler
app = Flask(__name__, static_url_path='/static')

json_handler = JsonHandler('events.json', 'profiles.json')
all_tags = ["Research",
"Photography",
"Art",
"Chess",
"Music",
"Robotics",
"Computer Science",
"Writing",
"Government/International Relations",
"Astronomy",
"Cybersecurity",
"Hackathon",
"Biology/Medicine"]

all_schools = list(set([school for profile in json_handler.profile_list for school in profile['schools']]))
all_events = [event['name'] for event in json_handler.event_list]
all_organisers = [event['organiser'] for event in json_handler.event_list]

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    
@app.route('/backup', methods=['GET'])
def backup():
    return render_template('backup home.html')


@app.route('/search_profiles', methods=['GET', 'POST'])
def search_profiles():
    if request.method == 'POST':
        
        search_terms = request.form.to_dict(flat=False)
        search_dict = {}
        for key, value in search_terms.items():
            if len(value) > 0:
                if key == 'tags':
                    search_dict[key ] = value
                elif value[0]:
                    search_dict[key] = value[0]

        result = json_handler.search_profiles(search_dict=search_dict)
    
        return render_template('search_profiles.html', tags = all_tags, schools=all_schools, search_dict = search_dict, profiles = result)
    else:
        return render_template('search_profiles.html', tags = all_tags, schools=all_schools)


@app.route('/search_events', methods=['GET', 'POST'])
def search_events():
    if request.method == 'POST':
        search_terms = request.form.to_dict(flat=False)
        search_dict = {}
        for key, value in search_terms.items():
            if len(value) > 0:
                if key == 'tags':
                    search_dict[key ] = value
                elif value[0]:
                    search_dict[key] = value[0]
        result = json_handler.search_events(search_dict=search_dict)

        
        print('SEARCH TERMS', search_terms)
        print('SEARCH DICT', search_dict)
        print('RESULT: ', result)
        
    
        return render_template('search_events.html', tags = all_tags, all_events=all_events, organisers=all_organisers, search_dict = search_dict, events = result)
    else:
        return render_template('search_events.html', tags = all_tags, all_events=all_events, organisers=all_organisers)


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
