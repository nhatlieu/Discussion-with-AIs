import os
import json
import pprint
import openai
from ai import AI

openApiKey = os.environ['OPEN_AI_KEY']

model = "gpt-3.5-turbo"

def save_combined_history(filename, user_first, user_follow):
    combined_content = user_first.get_content() + user_follow.get_content()
    combined_content = sorted(combined_content, key=lambda x: x.get('timestamp', 0))

    formatted_data = []
    for entry in combined_content:
        content = entry["content"]
        formatted_entry = f"{content}\n"
        formatted_data.append(formatted_entry)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(formatted_data))

formatSpecificationPrompt_op = open('system_op.pmpt', 'r', encoding = 'utf-8').read()
formatSpecificationPrompt_first = open('system_first.pmpt', 'r', encoding = 'utf-8').read()
formatSpecificationPrompt_follow = open('system_follow.pmpt', 'r', encoding = 'utf-8').read()

user_first = AI(openApiKey, model, "Mark", formatSpecificationPrompt_op)
user_follow = AI(openApiKey, model, "Sum", formatSpecificationPrompt_op)

load_choice = input("Do you want to load the previous conversation history? (y/n): ").lower()

if load_choice == 'y':
    topic_name = input("Enter the topic name for the history you want to load: ")
    history_filename_first = f"history_{topic_name}_first.json"
    history_filename_follow = f"history_{topic_name}_follow.json"

    if os.path.exists(history_filename_first) and os.path.exists(history_filename_follow):
        user_first.load_history(history_filename_first)
        user_follow.load_history(history_filename_follow)
        print("Previous conversation history loaded.")
    else:
        print(f"No history found for topic '{topic_name}'. Starting a new conversation.")
else:
    print("To start a new conversation, hit the ENTER button.")

user_first.add_system(formatSpecificationPrompt_first)
user_follow.add_system(formatSpecificationPrompt_follow)


response = ''
for i in range(1):
    user_input = input()
    if user_input:
        print("\n\n")
        response = user_first.create(user_input)
        print('\033[36m', response, '\033[0m\n\n\n')
    else: 
        response = user_first.create(response)
        print('\033[35m', response, '\033[0m\n\n\n')
        
    user_input_follow = input()
    if user_input_follow:
        print("\n\n")
        response = user_follow.create(user_input_follow)
        print('\033[36m', response, '\033[0m\n\n\n')
    else:
        response = user_follow.create(response)
        print('\033[36m', response, '\033[0m\n\n\n')


topic_name = input("Enter the topic name for saving: ")
if topic_name != "No":
    filename_first = f"history_{topic_name}_first.json"
    filename_follow = f"history_{topic_name}_follow.json"

    user_first.save_history(filename_first)
    user_follow.save_history(filename_follow)
    save_combined_history(f"combined_{topic_name}.json", user_first, user_follow)
    print("Conversation history saved.")
else:
    print("Conversation history has not being saved.")