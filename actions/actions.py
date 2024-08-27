# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# actions.py
# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import pandas as pd

# # Load the dataset
# df = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/universities.csv')

# class ActionUniversityRank(Action):
#     def name(self) -> Text:
#         return "action_university_rank"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         university = tracker.get_slot('university')
#         matched_rows = df[df['University_name'].str.contains(university, case=False, na=False)]
#         if not matched_rows.empty:
#             rank = matched_rows.iloc[0]['Rank']
#             response = f"{university} is ranked {rank}."
#         else:
#             response = "I couldn't find the ranking information for that university."

#         dispatcher.utter_message(text=response)
#         return []

# class ActionUniversityLocation(Action):
#     def name(self) -> Text:
#         return "action_university_location"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         university = tracker.get_slot('university')
#         matched_rows = df[df['University_name'].str.contains(university, case=False, na=False)]
#         if not matched_rows.empty:
#             location = matched_rows.iloc[0]['Location']
#             response = f"{university} is located in {location}."
#         else:
#             response = "I couldn't find the location for that university."

#         dispatcher.utter_message(text=response)
#         return []

# class ActionUniversityFee(Action):
#     def name(self) -> Text:
#         return "action_university_fee"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         university = tracker.get_slot('university')
#         matched_rows = df[df['University_name'].str.contains(university, case=False, na=False)]
#         if not matched_rows.empty:
#             fee = matched_rows.iloc[0]['Fee']
#             response = f"The tuition fee for {university} is {fee}."
#         else:
#             response = "I couldn't find the fee information for that university."

#         dispatcher.utter_message(text=response)
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

df = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/universities.csv')

class ActionUniversityRank(Action):
    def name(self) -> Text:
        return "action_university_rank"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        university = tracker.get_slot('university')
        # university = "Lancaster University"
        print("university",university)
        matched_rows = df[df['University_name'].str.contains(university, case=False, na=False)]
        if not matched_rows.empty:
            rank = matched_rows.iloc[0]['UK_rank']
            response = f"{university} is ranked {rank}."
        else:
            response = "I couldn't find the ranking information for that university."

        dispatcher.utter_message(text=response)
        return []