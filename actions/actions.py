import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
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
        from datetime import datetime
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
    def __init__(self):
        try:
            self.df_universities = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/uk_universities.csv', encoding='ISO-8859-1')
        except UnicodeDecodeError:
            self.df_universities = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/uk_universities.csv', encoding='utf-8')

    def name(self) -> Text:
        return "action_provide_university_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        university_name = tracker.get_slot('university_name')
        # Fetch university details from CSV
        university_details = self.df_universities[self.df_universities['University_name'].str.contains(university_name, case=False, na=False)]
        if not university_details.empty:
            details = university_details.iloc[0].to_dict()
            response = (f"Details for {details['University_name']}:\n"
                        f"Founded year: {details['Founded_year']}\n"
                        f"UK rank: {details['UK_rank']}\n"
                        f"World rank: {details['World_rank']}\n"
                        f"Minimum IELTS score: {details['Minimum_IELTS_score']}\n"
                        f"UG average fees: {details['UG_average_fees_(in_pounds)']}\n"
                        f"PG average fees: {details['PG_average_fees_(in_pounds)']}\n"
                        f"Website: {details['Website']}")
        else:
            response = f"Sorry, I couldn't find details for {university_name}."
        dispatcher.utter_message(text=response)
        return []


class ActionProvideMinimumIELTSScore(Action):
    def __init__(self):
        try:
            self.df_universities = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/uk_universities.csv', encoding='ISO-8859-1')
        except UnicodeDecodeError:
            self.df_universities = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/uk_universities.csv', encoding='utf-8')

    def name(self) -> Text:
        return "action_provide_minimum_ielts_score"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        university_name = tracker.get_slot('university_name')
        # Fetch IELTS score from CSV
        university_details = self.df_universities[self.df_universities['University_name'].str.contains(university_name, case=False, na=False)]
        if not university_details.empty:
            score = university_details.iloc[0]['Minimum_IELTS_score']
            response = f"The minimum IELTS score for {university_name} is {score}."
        else:
            response = f"Sorry, I couldn't find the IELTS score for {university_name}."
        dispatcher.utter_message(text=response)
        return []


class ActionProvideVisaRequirements(Action):
    def __init__(self):
        try:
            self.df_visas = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/visa.csv', encoding='ISO-8859-1')
        except UnicodeDecodeError:
            self.df_visas = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/visa.csv', encoding='utf-8')

    def name(self) -> Text:
        return "action_provide_visa_requirements"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        visa_type = tracker.get_slot('visa_type')
        # Fetch visa requirements from CSV
        visa_details = self.df_visas[self.df_visas['Accepetd Visa\'s'].str.contains(visa_type, case=False, na=False)]
        if not visa_details.empty:
            requirements = visa_details.iloc[0].dropna().to_dict()
            response = (f"Visa requirements for {visa_type}:\n"
                        f"{requirements['Requirement1']}\n"
                        f"{requirements['Requirement2']}\n"
                        f"{requirements['Requirement3']}\n"
                        f"{requirements['Requirement 4']}\n"
                        f"Duration: {requirements['Duration']}")
        else:
            response = f"Sorry, I couldn't find visa requirements for {visa_type}."
        dispatcher.utter_message(text=response)
        return []


class ActionProvideBestUniversity(Action):
    def __init__(self):
        try:
            self.df_universities = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/uk_universities.csv', encoding='ISO-8859-1')
        except UnicodeDecodeError:
            self.df_universities = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/uk_universities.csv', encoding='utf-8')

    def name(self) -> Text:
        return "action_provide_best_university"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        region = tracker.get_slot('region')
        # Fetch best university based on region
        universities_in_region = self.df_universities[self.df_universities['Region'].str.contains(region, case=False, na=False)]
        if not universities_in_region.empty:
            best_university = universities_in_region.sort_values(by='UK_rank').iloc[0]['University_name']
            response = f"The best university in {region} is {best_university}."
        else:
            response = f"Sorry, I couldn't find the best university in {region}."
        dispatcher.utter_message(text=response)
        return []
