from gettext import find
import json
from copy import deepcopy

class JsonHandler:
    def __init__(self, event_path, profile_path):
        self.event_path = event_path
        self.profile_path = profile_path

        self.profile_list = json.load(open(self.profile_path, 'rb'))
        self.event_list = json.load(open(self.event_path, 'rb'))
    
    def get_event_by_name(self, name):
        for event in self.event_list:
            if event['name'] == name:
                return event

    def get_profile_by_name(self, name):
        for profile in self.profile_list:
            if profile['name'] == name:
                return profile

    def search_profiles(self, search_dict):
        '''
        search_dict may contain name, school or tags
        '''

        result = deepcopy(self.profile_list)
        if 'name' in search_dict:
            result = list(filter(lambda profile: profile['name'] == search_dict['name'], result))
        
        if 'school' in search_dict:
            result = list(filter(lambda profile: search_dict['school'] in profile['schools'], result))

        if 'tags' in search_dict:
            result = list(filter(lambda profile: len(set(search_dict['tags']) & set(profile['tags'])) > 0, result))

        return result

    def search_events(self, search_dict):
        '''
        search_dict may contain name, organiser or tags
        '''

        result = deepcopy(self.event_list)
        if 'name' in search_dict:
            result = list(filter(lambda event: event['name'] == search_dict['name'], result))
        
        if 'organiser' in search_dict:
            result = list(filter(lambda event: search_dict['organiser'] == event['organiser'], result))

        if 'tags' in search_dict:
            result = list(filter(lambda event: event['tag'] in search_dict['tags'], result))

        return result


    