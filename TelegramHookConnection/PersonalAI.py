import openai, json, base64
import os
from . import GetRules, getRoles, ProgrammerBackground

MODEL = "gpt-3.5-turbo"

openai.api_key = os.environ.get('API_KEY')

roles = getRoles.ParseData()

def GetContext():
    with open('HisDetails.txt', 'r') as encoded_file:
        encoded_data = encoded_file.read()
        decoded_data = base64.b64decode(encoded_data)
        json_data = decoded_data.decode()
        return json.loads(json_data)

def make_chat_completion_request(question, rules, developer_Background):
    
    def place_Backround_And_Rules(DeveloperBackground, rules_to_follow):
        Background = ProgrammerBackground.ParseData()
        Principles = [
            {"role": "system", "content": Background[0] + rules_to_follow},
            {"role": "system", "content": Background[1] + DeveloperBackground},
            *roles,
        ]
        return Principles

    allPrinciples = place_Backround_And_Rules(developer_Background, rules)

    try:

        response = openai.ChatCompletion.create(
            model=MODEL,

            messages=[

                *allPrinciples,
                {"role": "user", "content": question},
                
            ],

            temperature=1,
            )
        return response['choices'][0]['message']['content']

    except:
        return None

about_developer = GetContext()
rules = GetRules.ParseData()

def Request_Question(question):
    response_rules = f"{rules.get('rule_1')}, {rules.get('rule_2', None)}, {rules.get('rule_3', None)}, {rules.get('rule_4', None)}, {rules.get('rule_5', None)}, {rules.get('rule_6', None)}"
    AI_request_result = make_chat_completion_request(question=question, rules=response_rules, developer_Background=about_developer)
    return AI_request_result