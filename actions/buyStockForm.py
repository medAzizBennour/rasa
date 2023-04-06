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

