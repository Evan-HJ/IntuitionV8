import json
from pathlib import Path


class JsonHandler:
    def __init__(self, event_path, profile_path):
        self.event_path = Path(event_path)
        self.profile_path = Path(profile_path)

        with self.profile_path.open(encoding="utf-8") as profile_file:
            self.profile_list = json.load(profile_file)

        with self.event_path.open(encoding="utf-8") as event_file:
            self.event_list = json.load(event_file)

    def get_event_by_name(self, name):
        for event in self.event_list:
            if event["name"].casefold() == name.casefold():
                return event
        return None

    def get_profile_by_name(self, name):
        for profile in self.profile_list:
            if profile["name"].casefold() == name.casefold():
                return profile
        return None

    def search_profiles(self, search_dict):
        """Filter profiles by partial name, school, and one or more interests."""
        result = list(self.profile_list)

        if "name" in search_dict:
            query = search_dict["name"].casefold()
            result = [profile for profile in result if query in profile["name"].casefold()]

        if "school" in search_dict:
            school = search_dict["school"].casefold()
            result = [
                profile
                for profile in result
                if any(school == item.casefold() for item in profile["schools"])
            ]

        if "tags" in search_dict:
            tags = {tag.casefold() for tag in search_dict["tags"]}
            result = [
                profile
                for profile in result
                if tags.intersection(tag.casefold() for tag in profile["tags"])
            ]

        return result

    def search_events(self, search_dict):
        """Filter events by partial name, partial organiser, and category."""
        result = list(self.event_list)

        if "name" in search_dict:
            query = search_dict["name"].casefold()
            result = [event for event in result if query in event["name"].casefold()]

        if "organiser" in search_dict:
            organiser = search_dict["organiser"].casefold()
            result = [
                event for event in result if organiser in event["organiser"].casefold()
            ]

        if "tags" in search_dict:
            tags = {tag.casefold() for tag in search_dict["tags"]}
            result = [event for event in result if event["tag"].casefold() in tags]

        return result
