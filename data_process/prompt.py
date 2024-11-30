import pandas as pd

def create_prompts(df, sys_prompt): 
    user_prompt = """
    Ballot question:
    <TITLE>
    <BALLOTQ>

    Decision:"""

    df["System"] = sys_prompt

    df["User"] = user_prompt

    #Replace tokens with values from columns
    df["System"] = df.apply(lambda row: row["System"].replace("<STATE>", row["State"]), axis=1)
    df["User"] = df.apply(lambda row: row["User"].replace("<TITLE>", row["Title"]), axis=1)
    df["User"] = df.apply(lambda row: row["User"].replace("<BALLOTQ>", row["Summary"]), axis=1)

    df = df[["System", "User"]]
    return df


df = pd.read_csv("./data/clean_ballot_qs.csv", index_col=0)

#Fixing a problem with a title that is a number
df["Title"] = df["Title"].astype(str)

#Define a prompt
sys_prompt_yn = "You are a voter from <STATE>. Please think step by step and consider the impact of the following ballot question on <STATE>. Then, make a final decision on how you will vote on the ballot question. Output your final decision in the form [[yes]] or [[no]]."
sys_prompt_ny = "You are a voter from <STATE>. Please think step by step and consider the impact of the following ballot question on <STATE>. Then, make a final decision on how you will vote on the ballot question. Output your final decision in the form [[no]] or [[yes]]."

prompts_yn = create_prompts(df, sys_prompt_yn)

prompts_yn.to_csv("./data/prompts_yn.csv")

prompts_ny = create_prompts(df, sys_prompt_ny)
prompts_ny.to_csv("./data/prompts_ny.csv")
