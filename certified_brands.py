import pandas as pd

#start span
df = pd.read_csv("certified_brands.csv")

#span 5
search_name = input("Enter brand to audit : ")

#[span_6]
is_certified = df['brand_name'].str.contains(search_name,case = False).any()

#result logic
if is_certified:
    print(f"success! {search_name} is a verified sustainable brand.")
else:
    print(f"Warnig: {search_name} was not found in our certified database.")