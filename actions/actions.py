from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
from rasa_sdk.events import SlotSet
from fuzzywuzzy import process


df = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/universities.csv')

class ActionDynamicGreet(Action):

    def name(self) -> Text:
        return "action_dynamic_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text')

        response = f"{user_message.capitalize()}! I am here to help you get the university details in the United Kingdom."

        dispatcher.utter_message(text=response)
        
        return []

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
        return []


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
    
class ActionFetchUniversityRank(Action):

    def name(self) -> Text:
        return "action_fetch_university_rank"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract the university name entity from the user's input
        university_name = tracker.get_slot('university_name')

        # Handle missing or None university name
        if not university_name:
            dispatcher.utter_message(text="I couldn't find a university name in your request.")
            return []

        # Find the university rank from the DataFrame
        rank = self.get_university_rank(university_name)
        
        # Create a response message based on the rank
        if rank:
            response = f"The rank of {university_name} is {rank}."
        else:
            response = f"I couldn't find the rank for {university_name}."
        
        dispatcher.utter_message(text=response)
        return [SlotSet('university_name', None)]

    @staticmethod
    def get_university_rank(university_name: Text) -> Any:
        # Query the DataFrame for the university's rank
        try:
            # Perform a case-insensitive search for the university name
            university_row = df[df['University_name'].str.contains(university_name, case=False, na=False)]
            if not university_row.empty:
                return university_row.iloc[0]['World_rank']  # Adjust column name if necessary
            else:
                return None
        except Exception as e:
            print(f"Error fetching university rank: {e}")
            return None
        
        
class ActionFetchBestRankedUniversity(Action):

    def name(self) -> Text:
        return "action_fetch_best_ranked_university"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        region = tracker.get_slot('region')

        # Find the best-ranked university in the specified region
        best_university = self.get_best_ranked_university(region)
        
        if best_university:
            response = f"The best-ranked university in {region} is {best_university}."
        else:
            response = f"I couldn't find the best-ranked university in {region}."
        
        dispatcher.utter_message(text=response)
        return []

    @staticmethod
    def get_best_ranked_university(region: Text) -> Any:
        # Query the DataFrame for the best-ranked university in the specified region
        try:
            region_universities = df[df['region'].str.lower() == region.lower()]
            if not region_universities.empty:
                best_university = region_universities.sort_values(by='World_rank').iloc[0]['University_name']
                return best_university
            else:
                return None
        except Exception as e:
            print(f"Error fetching best-ranked university: {e}")
            return None
