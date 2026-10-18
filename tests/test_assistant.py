import unittest

from jarvis.core.assistant import Assistant
from jarvis.core.state import AssistantState


class FakeAI:
    def chat(self, messages):
        return "local response"

    def list_models(self):
        return ["llama3.2:3b"]


class FakeApps:
    def open_app(self, name):
        return f"fake open: {name}"


class AssistantTests(unittest.TestCase):
    def setUp(self):
        self.state = AssistantState()
        self.assistant = Assistant(ai=FakeAI(), state=self.state, apps=FakeApps(), vision_model="")

    def test_stop_stops_session(self):
        response = self.assistant.handle("stop")
        self.assertFalse(self.state.running)
        self.assertIn("Stopping", response)

    def test_open_uses_app_router(self):
        self.assertEqual(self.assistant.handle("open notepad"), "fake open: notepad")

    def test_general_chat_is_remembered(self):
        self.assertEqual(self.assistant.handle("hello"), "local response")
        self.assertEqual(self.state.conversation[-1]["role"], "assistant")

    def test_screen_analysis_requires_local_vision_model(self):
        response = self.assistant.handle("what am I looking at")
        self.assertIn("image understanding is disabled", response)


if __name__ == "__main__":
    unittest.main()
