import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

#Example JSONL form for requests
#{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
#{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are an unhelpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}


def make_batch_jsonl(df1, df2):

    loop=-1
    for df in [df1, df2]:
        for _ in range(5): 
            loop+=1
            tasks = []
            for index, row in df.iterrows():                
                sys_prompt = row["System"]
                description = row['User']
                
                task = {
                    "custom_id": f"task-{loop}-{index}",
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        # This is what you would have in your Chat Completions API call
                        "model": "gpt-4o-mini",
                        "temperature": 0.7, #Default ChatGPT
                        "messages": [
                            {
                                "role": "system",
                                "content": sys_prompt
                            },
                            {
                                "role": "user",
                                "content": description
                            }
                        ], 
                        "max_tokens" : 1024
                    }
                }
            
                tasks.append(task)

        # Creating the file

            with open(f'./data/gpt/gpt_prompts_{loop}.jsonl', 'w') as file:
                for obj in tasks:
                    file.write(json.dumps(obj) + '\n')

def send_batch(round): 
    load_dotenv()

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    batch_input_file = client.files.create(
    file=open(f"./data/gpt/gpt_prompts_{round}.jsonl", "rb"),
    purpose="batch"
    )

    batch_input_file_id = batch_input_file.id

    client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
        "description": f"politics_{round}"
        }
    )

def test():
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a voter from Alabama. Please think step by step and consider the impact of the following ballot question on Alabama. Then, make a final decision on how you will vote on the ballot question. Output your final decision in the form [[yes]] or [[no]]."}, {"role": "user", "content": "\n    Ballot question:\n    Abolish the prohibition of interracial marriages\n    Legislative Constitutional Amendment<BR>  Proposing an amendment to the Constitution of Alabama of 1901, to abolish the prohibition of interracial marriages. (Proposed by Act No. 1999-321)\n\n    Decision:"},
        ], 
        max_tokens=1024
    )
    return response.choices[0].message.content

# df_yn = pd.read_csv('./data/prompts_yn.csv')
# df_ny = pd.read_csv('./data/prompts_ny.csv')

# make_batch_jsonl(df_yn, df_ny)
# print("done")

#Note: I can submit 2 batches at a time
#BATCHES SENT: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# round = 9

# send_batch(round)
