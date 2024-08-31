from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
from rasa_sdk.events import SlotSet

df = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/universities.csv')

class ActionUniversityRank(Action):
    def name(self) -> Text:
        return "action_find_university_rank"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        university = tracker.get_slot('university')
        matched_rows = df[df['University_name'].str.contains(university, case=False, na=False)]
        if not matched_rows.empty:
            rank = matched_rows.iloc[0]['UK_rank']
            response = f"{university} univeristy rank is {rank},"
        else:
            response = "I couldn't find the ranking information for that university."

        dispatcher.utter_message(text=response)
        return [SlotSet("university_rank_found", True)]


class ActionFindUniversitiesByRegion(Action):

    def name(self) -> Text:
        return "action_find_universities_by_region"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract region entity from the user's message
        region = tracker.get_slot("region")
        
        # Check if the region is not None
        if region:
            # Filter universities by region
            filtered_df = df[df['region'].str.lower() == region.lower()]

            # Get the list of universities in the specified region
            universities = filtered_df['name'].tolist()

            if universities:
                response = f"The universities in {region} are: {', '.join(universities)}."
            else:
                response = f"Sorry, I couldn't find any universities in {region}."
        else:
            response = "Please specify a region to search for universities."

        dispatcher.utter_message(text=response)
        return []