import os
import json
import pandas as pd
from mistralai import Mistral
from dotenv import load_dotenv


def make_batch_jsonl(df1, df2):

    loop=-1
    tasks = []

    for df in [df1, df2]:
        for _ in range(5): 
            loop+=1
            for index, row in df.iterrows():                
                sys_prompt = row["System"]
                description = row['User']
                
                task = {
                    "custom_id": f"task-{loop}-{index}",
                    "body": {
                        # This is what you would have in your Chat Completions API call
                        "model": "mistral-small-latest",
                        "temperature": 0.7, #Default Mistral Small
                        "max_tokens" : 1024,
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
                    }
                }
            
                tasks.append(task)

        # Creating the file

    with open(f'./data/mistral/mistral_prompts_all.jsonl', 'w') as file:
        for obj in tasks:
            file.write(json.dumps(obj) + '\n')


def send_batch(name, file): 
    load_dotenv()

    client = Mistral(
        api_key=os.environ.get("MISTRAL_API_KEY")
    )

    batch_data = client.files.upload(
    file={
        "file_name": name,
        "content": open(file, "rb")},
    purpose = "batch")
    
    created_job = client.batch.jobs.create(
        input_files=[batch_data.id],
        model="mistral-small-latest",
        endpoint="/v1/chat/completions",
        metadata={"job_type": "testing"}
        )
    
    retrieved_job = client.batch.jobs.get(job_id=created_job.id)

    print(retrieved_job)

load_dotenv()

client = Mistral(
    api_key=os.environ.get("MISTRAL_API_KEY")
)

list_job = client.batch.jobs.list(
    status="RUNNING",   
    metadata={"job_type": "testing"}
)

print(list_job)

retrieved_job = client.batch.jobs.get(job_id="26cbd211-f4aa-42ca-8e80-964346be7698")

client.files.download(file_id=retrieved_job.output_file)
#send_batch("test", "./data/mistral/test.jsonl")


# df_yn = pd.read_csv('./data/prompts_yn.csv')
# df_ny = pd.read_csv('./data/prompts_ny.csv')

# make_batch_jsonl(df_yn, df_ny)
# print("done")