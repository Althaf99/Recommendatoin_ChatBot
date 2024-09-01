import pandas as pd

# Step 1: Read the dataset
df = pd.read_csv('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/actions/universities.csv')

# Step 2: Extract the university names
university_names = df['University_name'].tolist()

# Step 3: Write the university names to a lookup file
with open('/Users/althafazad/Documents/Personal Projects/Recommendatoin_ChatBot/data/lookups/universities_lookup.txt', 'w') as f:
    for name in university_names:
        f.write(f'{name}\n')

print("Lookup file created successfully.")
