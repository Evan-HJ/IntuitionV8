# GROWTH+

**Helping students discover experiences that strengthen their portfolios.**

GROWTH+ is a web platform for pre-university students to find competitions, programmes, and extracurricular opportunities aligned with their interests. Students can also explore the paths taken by their peers and seniors, making it easier to identify worthwhile next steps.

The project was designed and built by a three-person student team during the 24-hour [iNTUition v8.0](https://intuition-v8.devpost.com/) hackathon in February 2022.

![GROWTH+ homepage](docs/images/growth-home.png)

## What it does

- Browse a catalogue of academic, creative, technical, and leadership opportunities.
- Search events by name or organiser and filter them by category.
- Search student profiles by name, school, and interests.
- Move between linked profile and event pages to explore shared experiences.
- Use autocomplete-assisted search to find schools and events quickly.
- Present the experience through a responsive Bootstrap interface.

The demonstration dataset contains **41 events**, **100 student profiles**, and **13 interest categories**, providing enough variety to exercise the platform's search and discovery flows.

## Product views

| Student profile | Event details |
| --- | --- |
| ![Student profile showing education, interests, and events](docs/images/growth-profile.png) | ![Event page showing its category, rating, and participants](docs/images/growth-event.png) |

## How it works

Flask handles routing and server-side rendering, while Jinja templates assemble the interface from structured JSON data. A dedicated `JsonHandler` provides profile and event lookup and applies combinations of name, school, organiser, and interest filters. The resulting records are rendered into cross-linked pages, with lightweight JavaScript providing autocomplete interactions in the search experience.

## Technology

- **Backend:** Python, Flask
- **Templating:** Jinja
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 4
- **Data:** JSON
- **Collaboration:** Git and GitHub

## Run locally

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependency:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   python server.py
   ```

4. Visit [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Project structure

```text
.
├── server.py          # Flask routes and application entry point
├── json_handler.py    # Search and data-access logic
├── events.json        # Demonstration event catalogue
├── profiles.json      # Demonstration student profiles
├── templates/         # Jinja page templates
└── static/            # Styles, JavaScript, and image assets
```

## Built in 24 hours

Within the hackathon window, the team moved from problem definition to a working, navigable prototype: shaping the product concept, creating a connected demonstration dataset, implementing multi-field search, and building the complete web interface.

Built by Evan Lim, Koh Jia Hng, and SYY. Evan's work focused on the frontend implementation and interaction design, including the styling system, search interfaces, autocomplete behaviour, and profile experience.
