import anthropic
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.beta.messages.batch_create_params import Request
import os
import pandas as pd
from dotenv import load_dotenv

def make_batch_requests(df1, df2):

    requests_list = []

    loop=-1
    for df in [df1, df2]:
            for _ in range(5): 
                loop+=1
                requests = []
                for index, row in df.iterrows():                
                    sys_prompt = row["System"]
                    description = row['User']
                    
                    request = Request(
                        custom_id=f"task-{loop}-{index}",
                        params=MessageCreateParamsNonStreaming(
                            model="claude-3-haiku-20240307",
                            max_tokens=1024,
                            system = sys_prompt,
                            messages=[
                                {
                                    "role": "user",
                                    "content": description
                                }
                            ], 
                        )
                    )
                    requests.append(request)
                requests_list.append(requests)

    return requests_list


def send_batch(requests): 
    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(
        api_key=api_key
    )

    message_batch = client.beta.messages.batches.create(
        requests=requests
    )

    print(message_batch)
     

df_yn = pd.read_csv('./data/prompts_yn.csv')
df_ny = pd.read_csv('./data/prompts_ny.csv')

request_list = make_batch_requests(df_yn, df_ny)


# for round in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:

#     send_batch(request_list[round])
