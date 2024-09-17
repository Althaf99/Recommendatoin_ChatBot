from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
from rasa_sdk.events import SlotSet
from fuzzywuzzy import fuzz, process


df = pd.read_csv('/actions/uk_universities.csv')

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


class ActionProvideUniversityDetails(Action):

    def name(self) -> Text:
        return "action_provide_university_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        university_name = next(tracker.get_latest_entity_values("university_name"), None)
        print("university_name", university_name)
        if university_name:
            university_details = self.get_university_details(university_name)
            
            if university_details:
                response = (f"The {university_name} is located {university_details['region']} "
                            f"holding the {university_details['rank']} in the UK. "
                            f"For more details, visit their official webpage {university_details['Website']}.")
            else:
                response = f"Sorry, I couldn't find details for {university_name}. Please check the name and try again."
        else:
            response = "Please provide a university name."

        dispatcher.utter_message(text=response)

        return []

    def get_university_details(self, university_name: Text) -> Dict[Text, Any]:
        all_universities = df['University_name'].tolist()
        
        best_match, score = process.extractOne(university_name, all_universities, scorer=fuzz.token_sort_ratio)
        
        if score >= 80:
            university_info = df[df['University_name'] == best_match]
            if not university_info.empty:
                details = university_info.iloc[0]
                return {
                    'region': details['Region'],
                    'rank': details['UK_rank'],
                    'Website': details['Website']  # Ensure your CSV has a column for the URL
                }
        return {}
    

# class ActionProvideUniversityListOnRegion(Action):

#     def name(self) -> Text:
#         return "action_provide_university_list_on_region"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # Extract region entity from the latest user message
#         region = next(tracker.get_latest_entity_values("region"), None)
#         print("region:", region)
        
#         if region:
#             # Get the list of universities in the specified region
#             universities = self.get_universities_in_region(region)
            
#             if universities:
#                 university_list = ', '.join(universities)
#                 response = f"The universities in {region} are: {university_list}."
#             else:
#                 response = f"Sorry, I couldn't find any universities in {region}."
#         else:
#             response = "Please provide a region."

#         dispatcher.utter_message(text=response)

#         return []

    # def get_universities_in_region(self, region: Text) -> List[Text]:
    #     # Search for universities in the given region
    #     universities_in_region = df[df['Region'].str.contains(region, case=False, na=False)]
        
    #     # Return the list of university names if any are found
    #     if not universities_in_region.empty:
    #         return universities_in_region['University_name'].tolist()
    #     return []
    


# class ActionAskRegion(Action):

#     def name(self) -> Text:
#         return "action_ask_region"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         region = tracker.get_slot('region')
#         if not region:
#             dispatcher.utter_message(template="utter_ask_region")
#         return []

class ActionProvideBestUniversity(Action):

    def name(self) -> Text:
        return "action_provide_best_university"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        region = tracker.get_slot('region')
        if region:
            # Assuming the DataFrame has columns 'Region' and 'University' with rank as an index
            best_university = df[df['Region'].str.contains(region, case=False)].sort_values('UK_rank').iloc[0]
            university_name = best_university['University_name']
            
            dispatcher.utter_message(
                template="utter_best_university",
                university_name=university_name,
                region=region
            )
            return [SlotSet("region", region)]
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any universities in that region.")
            return []
    


class ActionProvideMinimumIELTSScore(Action):

    def name(self) -> str:
        return "action_provide_minimum_ielts_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Get the university name from the user's message
        university = next(tracker.get_latest_entity_values("university"), None)
        
        if not university:
            dispatcher.utter_message(text="Please specify the university.")
            return []

        # Find the minimum IELTS score for the specified university
        result = df[df['institution'].str.lower() == university.lower()]
        
        if not result.empty:
            min_ielts_score = result['Minimum_IELTS_score'].values[0]
            dispatcher.utter_message(text=f"The minimum IELTS score for {university} is {min_ielts_score}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find the minimum IELTS score for {university}.")

        return []