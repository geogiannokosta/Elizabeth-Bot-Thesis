import pathlib, datetime, nltk
from typing import Any, Text, Dict, List

import datetime as dt
from datetime import date, datetime, timedelta

import json

import os 
import glob
import analysis

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import ReminderScheduled, ReminderCancelled
from rasa_sdk.forms import FormAction

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from rasa_sdk.events import SlotSet

class ValidateProfileInfoForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_profile_info_form"
   
    async def required_slots(
        self, 
        slots_mapped_in_domain: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> List[Text]:
        """Check for 'confirm_cur_med' value."""
        d = {}
        d['first_name'] = tracker.get_slot("first_name")
        d['last_name'] = tracker.get_slot("last_name")
        d['age'] = tracker.get_slot("age")
        d['sex'] = tracker.get_slot("sex")
        d['cur_med'] = tracker.get_slot("cur_med")

        with open('profile.json', 'w') as f:
            f.write(json.dumps(d))

        if tracker.get_slot("confirm_cur_med") == True:
            return ["first_name", "last_name", "age", "sex", "confirm_cur_med", "cur_med"]
        else: 
            return ["first_name", "last_name", "age", "sex", "confirm_cur_med"]

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        """Validate 'first_name' value."""
        # If the name is super short, it might be wrong.
        print(f"Name given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"first_name": None}
        else:
            return {"first_name": slot_value}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        """Validate 'last_name' value."""
        # If the name is super short, it might be wrong.
        print(f"Name given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short last name. I'm assuming you mis-spelled.")
            return {"last_name": None}
        else:
            return {"last_name": slot_value}

    def validate_age(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        """Validate 'age' value."""
        # If the age is not a number, it is wrong.
        slot_value = int(slot_value)
        if type(slot_value) == int:
            return {"age": slot_value}
        else:
            dispatcher.utter_message(text=f"That's not a number. Are you avoiding the question?")
            return {"age": None}

class ValidateWellnessForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_wellness_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict"
      ) -> List[Text]:
        d = {}
        d['exercise'] = tracker.get_slot("exercise")
        d['sleep'] = tracker.get_slot("sleep")
        d['diet'] = tracker.get_slot("diet")
        d['stress'] = tracker.get_slot("stress")
        d['goal'] = tracker.get_slot("goal")
        d['confirm_medication'] = tracker.get_slot("confirm_medication")

        with open('wellness_form_logs/wfl-'+date.today().strftime("%Y-%m-%d")+'.json', 'w') as f:
            f.write(json.dumps(d))

        if tracker.get_slot("confirm_exercise") == True:
          return ["confirm_exercise", "exercise", "confirm_medication", "sleep", "diet", "stress", "goal"]
        else:
          return ["confirm_exercise", "confirm_medication", "sleep", "diet", "stress", "goal"]


class ValidateMentalHealthForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_mental_health_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict"
      ) -> List[Text]:
        # if tracker.get_slot("text") is not None:
        d = {}
        d['mentalq1'] = tracker.get_slot("mentalq1")
        d['mentalq2'] = tracker.get_slot("mentalq2")
        d['mentalq3'] = tracker.get_slot("mentalq3")
        d['mentalq4'] = tracker.get_slot("mentalq4")
        d['mentalq5'] = tracker.get_slot("mentalq5")
        d['mentalq6'] = tracker.get_slot("mentalq6")
        d['mentalq7'] = tracker.get_slot("mentalq7")
        d['mentalq8'] = tracker.get_slot("mentalq8")

        with open('mental_form_logs/mental-'+date.today().strftime("%Y-%m-%d")+'.json', 'w') as f:
            f.write(json.dumps(d))
                
        return ["mentalq1", "mentalq2", "mentalq3", "mentalq4", "mentalq5", "mentalq6", "mentalq7", "mentalq8"]

class ActionSetReminder(Action):
    """Schedules a reminder for the next day of the wellness form."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("I will remind you to continue the weekly report in 24 hours.")

        date = datetime.datetime.now() + datetime.timedelta(hours=24)

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            name="wellness_reminder",
            kill_on_user_message=False,
        )

        return [reminder]

class ActionReactToReminder(Action):
    """Reminds the user to fill the next day of the form."""

    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(f"Remember to do today's wellness check!!")

        return []

class ForgetReminders(Action):
    """Cancels all reminders."""

    def name(self) -> Text:
        return "action_forget_reminders"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Okay, I'll cancel all your reminders.")

        # Cancel all reminders
        return [ReminderCancelled()]

class ActionTime(Action):
    
    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return []

class ActionSentiment(Action):

    """Calls analysis.py to calculate sentiment. Gives different answers according to sentiment value."""

    def name(self) -> Text:
        return "action_sentiment"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        list_of_files = glob.glob('C:/Users/stath/Documents/Georgia/geobot/logs/*')
        latest_file = max(list_of_files, key=os.path.getctime)

        # average_sentiment = analysis.sentiment_avg(latest_file)
        # average_sentiment = analysis.sentiment_weight_avg(latest_file)
        average_sentiment = analysis.sentiment_weight2_avg(latest_file)
        # average_sentiment = analysis.sentiment_threshold_avg(latest_file)
        # average_sentiment = analysis.sentiment_confidence_avg(latest_file)

        if -1 <= average_sentiment <= -0.7:
            dispatcher.utter_message(text=f"My intuition says that you are having a rough time. If you want to talk to your doctor type: doctor")
        elif -0.7 < average_sentiment <= 0:
            dispatcher.utter_message(text=f"You seem a bit off. If you want to talk to your doctor type: doctor")
        elif 0 < average_sentiment <= 0.7:
            dispatcher.utter_message(text=f"I am sensing your good vibes! Keep it up!")
        elif 0.7 < average_sentiment <=1:
            dispatcher.utter_message(text=f"You are a walking sun of cheerfulness! Keep it up!")

        return []

class ActionHowToSentiment(Action):

    """Tells user which method was used to calculate their average sentiment."""

    def name(self) -> Text:
        return "action_how_to_sentiment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_of_files = glob.glob('C:/Users/stath/Documents/Georgia/geobot/logs/*')
        latest_file = max(list_of_files, key=os.path.getctime)
        
        # average_sentiment = analysis.sentiment_avg(latest_file)
        # average_weight_sentiment = analysis.sentiment_weight_avg(latest_file)
        average_weight2_sentiment = analysis.sentiment_weight2_avg(latest_file)
        # average_threshold_sentiment = analysis.sentiment_threshold_avg(latest_file)
        # average_confidence_sentiment = analysis.sentiment_confidence_avg(latest_file)

        # dispatcher.utter_message(text=f"I used magic to find out that your average sentiment throughout this conversation was {average_sentiment}")
        # dispatcher.utter_message(text=f"I used magic to find out that your average weighted sentiment throughout this conversation was {average_weight_sentiment}")
        dispatcher.utter_message(text=f"I used Machine Learning to find out that your average sentiment throughout this conversation was {average_weight2_sentiment}")
        # dispatcher.utter_message(text=f"I used magic to find out that your average sentiment (threshold) throughout this conversation was {average_threshold_sentiment}")
        # dispatcher.utter_message(text=f"I used magic to find out that your average sentiment (confidence weighted) throughout this conversation was {average_confidence_sentiment}")

        return []
