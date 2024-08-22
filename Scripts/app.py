import pandas as pd
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('cwurData.csv')  # Assuming your dataset is saved as 'universities.csv'

# Initialize the NLP model for zero-shot classification
nlp = pipeline("zero-shot-classification", model="facebook/bart-large-mnli",device=0)

def get_university_info(query):
    # Convert the query to lowercase for easier matching
    query_lower = query.lower()

    # Initialize response
    response = ""

    # Check if the query mentions a specific country
    if "in " in query_lower:
        # Extract country name
        country_start = query_lower.find("in ") + 3
        country_name = query_lower[country_start:].strip()

        # Filter the dataset by the specified country
        matched_rows = df[df['country'].str.contains(country_name, case=False, na=False)]

        if matched_rows.empty:
            response = f"No universities found in {country_name}."
        else:
            # Check if the query mentions "best" or similar keywords
            if "best" in query_lower or "top" in query_lower:
                # Sort by world rank and select the top result
                best_university = matched_rows.loc[matched_rows['world_rank'].idxmin()]
                response = (
                    f"The best university in {country_name} is "
                    f"{best_university['institution']} (Rank: {best_university['world_rank']})."
                )
            else:
                # Return all universities in the country
                response = f"Here are some universities in {country_name}:\n"
                for _, row in matched_rows.iterrows():
                    response += f"{row['institution']} (Rank: {row['world_rank']})\n"
    else:
        # Fallback: match query against institution names
        matched_rows = df[df['institution'].str.contains(query, case=False, na=False)]

        if not matched_rows.empty:
            response = "Here are some suggestions:\n"
            for _, row in matched_rows.iterrows():
                response += f"{row['institution']} (Rank: {row['world_rank']}, Country: {row['country']})\n"
        else:
            response = "No matching universities found in the dataset."

    return response


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # Zero-shot classification to understand the user query
    candidate_labels = list(df['institution'].unique())  # Use institution names as candidate labels
    nlp_result = nlp(user_input, candidate_labels)

    # The highest score label is our best guess
    best_label = nlp_result['labels'][0]

    # Generate a response based on the best label
    response = get_university_info(best_label)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
