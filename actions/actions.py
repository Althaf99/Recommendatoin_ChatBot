from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
from typing import Any, Text, Dict, List


class ActionHandleBotChallenge(Action):

    def name(self) -> Text:
        return "action_handle_bot_challenge"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Respond to the bot challenge intent
        dispatcher.utter_message(text="I am a bot, created by M.Shakir.")
        
        return []

class ActionDynamicGreet(Action):

    def name(self) -> Text:
        return "action_dynamic_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the current hour to determine the time of day
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good morning!"
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"

        # Generate a dynamic greeting message
        message = f"{greeting} I am here to help you get the university details in the United Kingdom."

        # Send the message to the user
        dispatcher.utter_message(text=message)

        return []


class ActionProvideUniversityDetails(Action):
    def name(self) -> str:
        return "action_provide_university_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> dict:
        university_name = tracker.get_slot('university_name')
        # Implement logic to fetch details from the dataset
        # Here is an example response
        details = f"Details for {university_name}: Founded year: 1209, UK rank: 1, World rank: 4."
        dispatcher.utter_message(text=details)
        return {}

class ActionProvideMinimumIELTSScore(Action):
    def name(self) -> str:
        return "action_provide_minimum_ielts_score"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> dict:
        university_name = tracker.get_slot('university_name')
        # Implement logic to fetch minimum IELTS score
        score = "6.5"  # Example score
        dispatcher.utter_message(text=f"The minimum IELTS score for {university_name} is {score}.")
        return {}

class ActionProvideVisaRequirements(Action):
    def name(self) -> str:
        return "action_provide_visa_requirements"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> dict:
        visa_type = tracker.get_slot('visa_type')
        # Implement logic to fetch visa requirements
        requirements = ("Job offer from a licensed UK employer. Minimum salary threshold (�26,200 or as specified)."
                        " English language proficiency (level B1). Certificate of Sponsorship from the employer."
                        " Up to 5 years (renewable; eligible for ILR after 5 years).")
        dispatcher.utter_message(text=f"Visa requirements for {visa_type}: {requirements}")
        return {}

class ActionProvideBestUniversity(Action):
    def name(self) -> str:
        return "action_provide_best_university"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> dict:
        region = tracker.get_slot('region')
        # Implement logic to find the best university based on region
        university = "University of Cambridge"  # Example university
        dispatcher.utter_message(text=f"The best university in {region} is {university}.")
        return {}
