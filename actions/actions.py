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
from rasa_sdk.forms import FormAction

class BuyStockForm(FormAction):
    def name(self) -> Text:
        return "buy_stock_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["stock_company", "stock_number"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "stock_company": [self.from_entity(entity="stock_company"), self.from_text()],
            "stock_number": [self.from_entity(entity="stock_number"), self.from_text()]
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        # Get the values of the slots
        stock_name = tracker.get_slot("stock_company")
        quantity = tracker.get_slot("stock_number")

        # Do something with the form data (e.g. submit to an API)
        # ...

        # Send the user a confirmation message
        message = f"You want to buy {quantity} shares of {stock_name}. Is that correct?"
        dispatcher.utter_message(message)

        # Reset the form
        return [SlotSet("stock_company", None), SlotSet("stock_number", None)]

