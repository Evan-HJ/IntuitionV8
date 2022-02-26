from flask import *
import json
from datetime import datetime
from json_handler import JsonHandler
app = Flask(__name__, static_url_path='/static')

json_handler = JsonHandler('events.json', 'profiles.json')
all_tags = ['A', 'B']

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

    
@app.route('/meetings', methods=['GET'])
def meetings():
    return render_template('meetings.html')

@app.route('/search_profiles', methods=['GET', 'POST'])
def search():
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
    
        return render_template('search_profile.html', tags = all_tags, search_dict = search_dict, profiles = result)
    else:
        return render_template('search_profile.html', tags = all_tags)

if (__name__ == '__main__'):
    app.run(debug=True)
