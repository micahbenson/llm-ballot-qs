import pandas as pd

#Read in Data
df = pd.read_csv("./data/general_election.csv")
#Convert FIPS code from 4-5 digit county level to 1-2 digit state level
df['STCOFIPS10'] = df['STCOFIPS10'].apply(lambda x: int(str(x)[:-3]))
#Identify state from FIPS code
def fips(num):
    match num:
        case 1: return "ALABAMA"
        case 2: return "ALASKA"
        case 4: return "ARIZONA"
        case 5: return "ARKANSAS"
        case 6: return "CALIFORNIA"
        case 8: return "COLORADO"
        case 9: return "CONNECTICUT"
        case 10: return "DELAWARE"
        case 11: return "DISTRICT OF COLUMBIA"
        case 12: return "FLORIDA"
        case 13: return "GEORGIA"
        case 15: return "HAWAII"
        case 16: return "IDAHO"
        case 17: return "ILLINOIS"
        case 18: return "INDIANA"
        case 19: return "IOWA"
        case 20: return "KANSAS"
        case 21: return "KENTUCKY"
        case 22: return "LOUISIANA"
        case 23: return "MAINE"
        case 24: return "MARYLAND"
        case 25: return "MASSACHUSETTS"
        case 26: return "MICHIGAN"
        case 27: return "MINNESOTA"
        case 28: return "MISSISSIPPI"
        case 29: return "MISSOURI"
        case 30: return "MONTANA"
        case 31: return "NEBRASKA"
        case 32: return "NEVADA"
        case 33: return "NEW HAMPSHIRE"
        case 34: return "NEW JERSEY"
        case 35: return "NEW MEXICO"
        case 36: return "NEW YORK"
        case 37: return "NORTH CAROLINA"
        case 38: return "NORTH DAKOTA"
        case 39: return "OHIO"
        case 40: return "OKLAHOMA"
        case 41: return "OREGON"
        case 42: return "PENNSYLVANIA"
        case 44: return "RHODE ISLAND"
        case 45: return "SOUTH CAROLINA"
        case 46: return "SOUTH DAKOTA"
        case 47: return "TENNESSEE"
        case 48: return "TEXAS"
        case 49: return "UTAH"
        case 50: return "VERMONT"
        case 51: return "VIRGINIA"
        case 53: return "WASHINGTON"
        case 54: return "WEST VIRGINIA"
        case 55: return "WISCONSIN"
        case 56: return "WYOMING"
df['STCOFIPS10'] = df['STCOFIPS10'].apply(lambda x: fips(x))

df = df[["STCOFIPS10","YEAR","PRES_DEM_VOTES","PRES_REP_VOTES"]]
df = df.dropna()
#Group data based on state and 4 year bin
df["GROUP"] = df["STCOFIPS10"] + df["YEAR"].astype(str)
df = df.groupby(["GROUP"]).sum().reset_index()
df = df[["GROUP","PRES_DEM_VOTES","PRES_REP_VOTES"]]
df["STATE"] = df["GROUP"].apply(lambda x: x[:-4])
df["YEAR"] = df["GROUP"].apply(lambda x: x[-4:])
#Add ratio of votes for dem and rep voting data
df["PRES_DEM_RATIO"] = df["PRES_DEM_VOTES"]/(df["PRES_DEM_VOTES"] + df["PRES_REP_VOTES"])
df["PRES_REP_RATIO"] = df["PRES_REP_VOTES"]/(df["PRES_DEM_VOTES"] + df["PRES_REP_VOTES"])
df = df[["STATE","YEAR","PRES_DEM_VOTES","PRES_REP_VOTES","PRES_DEM_RATIO","PRES_REP_RATIO"]]
#Save dataframe as csv
df.to_csv("./data/clean_general_election.csv")
