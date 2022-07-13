from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

import json
from datetime import date, datetime
import nltk

nltk.downloader.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

class SentimentAnalyzer(Component):
    """A pre-trained sentiment component"""

    name = "sentiment_analyzer"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["en"]

    @classmethod
    def required_packages(cls):
        return ["nltk"]
    
    def __init__(self, component_config=None):
        super(SentimentAnalyzer, self).__init__(component_config)
        self.today = date.today()
        self.now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def train(self, training_data, cfg, **kwargs):
        """Not needed, because the the model is pretrained"""
        pass

    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""
        
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "sentiment_extractor"}

        return entity

    def process(self, message, **kwargs):
        """Retrieve the text message, pass it to the classifier
            and append the prediction results to the message class."""

        sid = SentimentIntensityAnalyzer()
        res = sid.polarity_scores(str(message.get("text")))
        key, value = max(res.items(), key=lambda x: x[1])

        entity = self.convert_to_rasa(key, value)

        if message.get("text") is not None:
            d = {}
            d['timestamp'] = datetime.now().strftime("%H:%M:%S")
            d['msg'] = message.get("text")
            d['value'] = entity['value'] 
            d['confidence'] = entity['confidence'] 
            d['compound'] = res['compound'] 

            with open('logs/log-'+self.today.strftime("%Y-%m-%d")+'.json', 'a') as f:
                f.write(json.dumps(d))
                f.write("\n")
                
            with open('logs/log-'+self.now+'.json', 'a') as f:
                f.write(json.dumps(d))
                f.write("\n")

        message.set("entities", [entity], add_to_output=True)

    # def persist(self, model_dir):
    #     """Pass because a pre-trained model is already persisted"""
    #     pass