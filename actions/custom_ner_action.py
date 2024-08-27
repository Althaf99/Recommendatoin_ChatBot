# actions/custom_ner_action.py
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from transformers import pipeline
from typing import Any, Dict, List

class ActionExtractUniversity(Action):
    def name(self) -> str:
        return "action_extract_university"

    def __init__(self) -> None:
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = tracker.latest_message.get('text')
        ner_results = self.ner_pipeline(text)
        university_entities = [ent['word'] for ent in ner_results if ent['entity'] == 'B-ORG']
        
        if university_entities:
            response = f"I found these universities: {', '.join(university_entities)}"
        else:
            response = "I couldn't find any universities in your message."
        
        dispatcher.utter_message(text=response)
        return []
