import os
import json
import time
import random

def random_question(excludelist):
    """This is to generate a random questions and answer combined."""
    with open("data/questions_test.json", "r") as questions:
        data = json.load(questions)
        excluded = []
        for item, value in enumerate(data):
            if str(item) not in excludelist:
                excluded.append(value)
            
        return random.choice(excluded)
        

print(random_question(["0"]))        