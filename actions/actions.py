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
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import json

class ResetSlotsAction(Action):
    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        return [SlotSet("stock_company", None), SlotSet("stock_number", None)]

class BuyStockAction(Action):

    def name(self) -> Text:
        return "action_buy_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get latest user message
        latest_message = tracker.latest_message
        
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        stock_company = None
        stock_number = None
        
        for entity in latest_message['entities']:
            if entity['entity'] == 'stock_company':
                stock_company = entity['value']
            elif entity['entity'] == 'stock_number':
                stock_number = entity['value']
        
        # Save extracted entities in slots
        if stock_company:
            tracker.slots['stock_company'] = stock_company
        if stock_number:
            tracker.slots['stock_number'] = stock_number
        stock_number = tracker.get_slot("stock_number")
        stock_company = tracker.get_slot("stock_company")
        
        # Generate response message
        response_message = f"processing command..."
        response_dict = {"intent": intent, "entities": [{"stock_number":stock_number},{"stock_company":stock_company}], "response": response_message}

        # Send response message using dispatcher
        dispatcher.utter_message(json.dumps(response_dict))

        return [SlotSet("stock_company", stock_company), SlotSet("stock_number", stock_number)]
    
class NavigateAction(Action):

    def name(self) -> Text:
        return "action_navigate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get latest user message
        latest_message = tracker.latest_message
        
        # Get intent and extracted entities
        intent = latest_message['intent']['name']
        page = None
        
        for entity in latest_message['entities']:
            if entity['entity'] == 'page':
                page = entity['value']
        
        
        # Save extracted entities in slots
        if page:
            tracker.slots['page'] = page
        page = tracker.get_slot("page")
        
        # Generate response message
        response_message = f"navigating to {page}"
        response_dict = {"intent": intent, "entities": {"page":page}, "response": response_message}

        # Send response message using dispatcher
        dispatcher.utter_message(json.dumps(response_dict))

        return [SlotSet("page", page)]

