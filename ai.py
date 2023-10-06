import pprint
import openai
import json

class AI:
    def __init__(self, key:str, model:str, name:str, system_contents:str) -> None:
        openai.api_key = key
        self.model = model
        self.content = []
        self.name = name
        self.system_contents = [
            {"role": "system", "content": system_contents},
        ]

    def add_system(self, system_contents):
        self.system_contents.append({"role": "system", "content": system_contents})
    
    def create(self, message):
        self.content.append({"role": "user", "content": message, "name": self.name})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.system_contents + self.content,
        )

        assistant_content = str(response.choices[0]["message"]["content"])
        assistant_role = str(response.choices[0]["message"]["role"])

        formatted_response = f"{self.name}: {assistant_content}"
        self.content.append({"role": assistant_role, "content": assistant_content})

        return formatted_response
    
    def show(self):
        pprint.pprint(self.system_contents + self.content)

    def save_history(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.content, f)

    def load_history(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.content = json.load(f)

    def get_content(self):
        return self.content
