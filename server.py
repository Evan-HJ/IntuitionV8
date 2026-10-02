from pathlib import Path

from flask import Flask, abort, render_template, request

from json_handler import JsonHandler

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, static_url_path="/static")
json_handler = JsonHandler(BASE_DIR / "events.json", BASE_DIR / "profiles.json")

all_tags = [
    "Research",
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
    "Biology/Medicine",
]

all_schools = sorted(
    {school for profile in json_handler.profile_list for school in profile["schools"]}
)
all_profiles = sorted(profile["name"] for profile in json_handler.profile_list)
all_events = sorted(event["name"] for event in json_handler.event_list)
all_organisers = sorted({event["organiser"] for event in json_handler.event_list})


def get_search_filters():
    """Return non-empty search values from either a GET or POST request."""
    source = request.args if request.method == "GET" else request.form
    search_dict = {}

    for key in ("name", "school", "organiser"):
        value = source.get(key, "").strip()
        if value:
            search_dict[key] = value

    tags = [tag.strip() for tag in source.getlist("tags") if tag.strip()]
    if tags:
        search_dict["tags"] = tags

    return search_dict


@app.get("/")
def home():
    return render_template(
        "home.html",
        event_count=len(json_handler.event_list),
        profile_count=len(json_handler.profile_list),
        category_count=len(all_tags),
    )


@app.route("/search_profiles", methods=["GET", "POST"])
def search_profiles():
    search_dict = get_search_filters()
    profiles = json_handler.search_profiles(search_dict)

    return render_template(
        "search_profiles.html",
        tags=all_tags,
        schools=all_schools,
        profile_names=all_profiles,
        search_dict=search_dict,
        profiles=profiles,
    )


@app.route("/search_events", methods=["GET", "POST"])
def search_events():
    search_dict = get_search_filters()
    events = json_handler.search_events(search_dict)

    return render_template(
        "search_events.html",
        tags=all_tags,
        all_events=all_events,
        organisers=all_organisers,
        search_dict=search_dict,
        events=events,
    )


@app.get("/profile/<string:name>")
def show_profile(name):
    profile = json_handler.get_profile_by_name(name)
    if profile is None:
        abort(404)

    return render_template("profile.html", profile=profile)


@app.get("/event/<string:name>")
def show_event(name):
    event = json_handler.get_event_by_name(name)
    if event is None:
        abort(404)

    return render_template("event.html", event=event)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()
