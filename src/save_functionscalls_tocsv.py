import pandas as pd
data_set = pd.read_csv("C:/Users/Joseph Dania/Desktop/Ai_search_engine/raw_code.csv")
function_call = data_set["Function Calls"].astype(str).dropna()
too_csv = []
for name in function_call:
    name_s = name.strip()
    too_csv.append(name_s)
new_df = pd.DataFrame(too_csv, columns=["functions calls cleaned"])
new_df.to_csv("C:/Users/Joseph Dania/Desktop/Ai_search_engine/function_calls.csv", index=False)