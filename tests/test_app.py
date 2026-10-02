import re
import unittest

from server import app, json_handler


class GrowthAppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_main_pages_load(self):
        for path in ("/", "/search_profiles", "/search_events"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_catalogues_show_all_records_by_default(self):
        profile_page = self.client.get("/search_profiles").get_data(as_text=True)
        event_page = self.client.get("/search_events").get_data(as_text=True)

        self.assertIn("100 people", profile_page)
        self.assertIn("41 events", event_page)

    def test_profile_search_is_case_insensitive_and_combines_filters(self):
        response = self.client.get(
            "/search_profiles",
            query_string={"name": "ella", "school": "central jc", "tags": "Chess"},
        )
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ella-May Lopez", page)
        self.assertIn("1 person", page)

    def test_event_search_supports_partial_queries(self):
        response = self.client.get(
            "/search_events",
            query_string={"organiser": "singapore", "tags": "Robotics"},
        )
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("National Robotics Fair", page)
        self.assertIn("1 event", page)

    def test_legacy_post_search_still_works(self):
        response = self.client.post("/search_events", data={"tags": "Hackathon"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Whitehacks", response.get_data(as_text=True))

    def test_detail_pages_and_missing_records(self):
        self.assertEqual(self.client.get("/profile/Ella-May Lopez").status_code, 200)
        self.assertEqual(self.client.get("/event/Whitehacks").status_code, 200)
        self.assertEqual(self.client.get("/profile/Not A Person").status_code, 404)
        self.assertEqual(self.client.get("/event/Not An Event").status_code, 404)

    def test_form_ids_are_unique(self):
        for path in ("/search_profiles", "/search_events"):
            page = self.client.get(path).get_data(as_text=True)
            element_ids = re.findall(r'\sid="([^"]+)"', page)
            with self.subTest(path=path):
                self.assertEqual(len(element_ids), len(set(element_ids)))

    def test_primary_navigation_has_no_broken_internal_links(self):
        pages = (
            "/",
            "/search_profiles?name=Ella-May+Lopez",
            "/search_events?tags=Hackathon",
            "/profile/Ella-May%20Lopez",
            "/event/Whitehacks",
        )

        links = set()
        for page in pages:
            html = self.client.get(page).get_data(as_text=True)
            links.update(re.findall(r'href="(/[^"]*)"', html))

        for link in links:
            if link.startswith("/static/") or link.startswith("/#"):
                continue
            with self.subTest(link=link):
                self.assertNotEqual(self.client.get(link).status_code, 404)

    def test_profile_and_event_relationships_are_consistent(self):
        event_names = {event["name"] for event in json_handler.event_list}
        profile_names = {profile["name"] for profile in json_handler.profile_list}

        for profile in json_handler.profile_list:
            self.assertTrue(set(profile["events"]).issubset(event_names))

        for event in json_handler.event_list:
            self.assertTrue(set(event["participants"]).issubset(profile_names))


if __name__ == "__main__":
    unittest.main()
