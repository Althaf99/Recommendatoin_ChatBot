import pandas as pd
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('uk_universities.csv')  # Assuming your dataset is saved as 'universities.csv'

# Initialize the NLP model for zero-shot classification
nlp = pipeline("zero-shot-classification", model="facebook/bart-large-mnli",device=0)

def get_university_info(query):
    # Convert the query to lowercase for easier matching
    # query_lower = query.lower()

    # Initialize response
    # response = ""

    # # Check if the query mentions a specific country
    # if "in " in query_lower:
    #     # Extract country name
    #     country_start = query_lower.find("in ") + 3
    #     country_name = query_lower[country_start:].strip()

    #     # Filter the dataset by the specified country
    #     matched_rows = df[df['country'].str.contains(country_name, case=False, na=False)]

    #     if matched_rows.empty:
    #         response = f"No universities found in {country_name}."
    #     else:
    #         # Check if the query mentions "best" or similar keywords
    #         if "best" in query_lower or "top" in query_lower:
    #             # Sort by world rank and select the top result
    #             best_university = matched_rows.loc[matched_rows['world_rank'].idxmin()]
    #             response = (
    #                 f"The best university in {country_name} is "
    #                 f"{best_university['institution']} (Rank: {best_university['world_rank']})."
    #             )
    #         else:
    #             # Return all universities in the country
    #             response = f"Here are some universities in {country_name}:\n"
    #             for _, row in matched_rows.iterrows():
    #                 response += f"{row['institution']} (Rank: {row['world_rank']})\n"
    # else:
    #     # Fallback: match query against institution names
    #     matched_rows = df[df['institution'].str.contains(query, case=False, na=False)]

    #     if not matched_rows.empty:
    #         response = "Here are some suggestions:\n"
    #         for _, row in matched_rows.iterrows():
    #             response += f"{row['institution']} (Rank: {row['world_rank']}, Country: {row['country']})\n"
    #     else:
    #         response = "No matching universities found in the dataset."

    if "rank" in query.lower():
        response = get_university_ranking(query)
    elif "fee" in query.lower() or "cost" in query.lower():
        response = get_university_fees(query)
    elif "student satisfaction" in query.lower():
        response = get_student_satisfaction(query)
    elif "website" in query.lower():
        response = get_university_website(query)
    elif "IELTS" in query.lower():
        response = get_ielts_requirement(query)
    elif "international students" in query.lower():
        response = get_international_students_info(query)
    else:
        response = get_university_details(query)
    
    return response




@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # Zero-shot classification to understand the user query
    candidate_labels = list(df['University_name'].unique())  # Use institution names as candidate labels
    nlp_result = nlp(user_input, candidate_labels)

    # The highest score label is our best guess
    best_label = nlp_result['labels'][0]

    print("best_label",best_label)

    # Generate a response based on the best label
    response = get_university_info(user_input)

    return jsonify({'response': response})


# # Function to handle user queries
# def evaluate_query(user_input):
#     # Determine the type of question (ranking, fees, etc.)
#     if "rank" in user_input.lower():
#         response = get_university_ranking(user_input)
#     elif "fee" in user_input.lower() or "cost" in user_input.lower():
#         response = get_university_fees(user_input)
#     elif "student satisfaction" in user_input.lower():
#         response = get_student_satisfaction(user_input)
#     elif "website" in user_input.lower():
#         response = get_university_website(user_input)
#     elif "IELTS" in user_input.lower():
#         response = get_ielts_requirement(user_input)
#     elif "international students" in user_input.lower():
#         response = get_international_students_info(user_input)
#     else:
#         response = "I'm sorry, I don't understand the query. Could you please provide more details?"
    
#     return response


# Function to get university full details
def get_university_details(user_input):
    candidate_labels = [
        "University_name",
        "Region",
        "Founded_year",
        "Motto",
        "UK_rank",
        "World_rank",
        "Minimum_IELTS_score",
        "UG_average_fees_(in_pounds)"
    ]
    
    # Perform zero-shot classification
    nlp_result = nlp(user_input, candidate_labels)
    best_label = nlp_result['labels'][0]
    print("Best label:", best_label)
    
    # Retrieve the top score label's details
    university_info = ""
    
    if best_label in df.columns:
            # If asking for a university's name, provide some details
            # General case: find the best match for the user's query
            # Assuming we're always asking for "the best" in some aspect
            top_university = df[df[best_label] == df[best_label].min()].iloc[0]
            university_info = f"The university with the best {best_label} is {top_university['University_name']}, with a {best_label} of {top_university[best_label]}."
    return university_info


# # Function to get university ranking
def get_university_ranking(user_input):
    candidate_labels = list(df['University_name'].unique())
    nlp_result = nlp(user_input, candidate_labels)
    best_label = nlp_result['labels'][0]
    
    university_info = df[df['University_name'].str.contains(best_label, case=False, na=False)]
    if not university_info.empty:
        info = university_info.iloc[0]
        return f"{info['University_name']} is ranked {info['UK_rank']} in the UK and {info['World_rank']} in the world."
    else:
        return "No matching universities found."


# Function to get university fees
def get_university_fees(user_input):
    candidate_labels = list(df['University_name'].unique())
    nlp_result = nlp(user_input, candidate_labels)
    best_label = nlp_result['labels'][0]
    
    university_info = df[df['University_name'].str.contains(best_label, case=False, na=False)]
    if not university_info.empty:
        info = university_info.iloc[0]
        return (f"{info['University_name']} has an average undergraduate fee of £{info['UG_average_fees_(in_pounds)']} "
                f"and a postgraduate fee of £{info['PG_average_fees_(in_pounds)']} per year.")
    else:
        return "No matching universities found."

# Function to get student satisfaction
def get_student_satisfaction(user_input):
    candidate_labels = list(df['University_name'].unique())
    nlp_result = nlp(user_input, candidate_labels)
    best_label = nlp_result['labels'][0]
    
    university_info = df[df['University_name'].str.contains(best_label, case=False, na=False)]
    if not university_info.empty:
        info = university_info.iloc[0]
        return f"{info['University_name']} has a student satisfaction rate of {info['Student_satisfaction']}."
    else:
        return "No matching universities found."

# Function to get university website
def get_university_website(user_input):
    candidate_labels = list(df['University_name'].unique())
    nlp_result = nlp(user_input, candidate_labels)
    best_label = nlp_result['labels'][0]
    
    university_info = df[df['University_name'].str.contains(best_label, case=False, na=False)]
    if not university_info.empty:
        info = university_info.iloc[0]
        return f"You can find more information on the university's website: {info['Website']}."
    else:
        return "No matching universities found."

# Function to get IELTS requirement
def get_ielts_requirement(user_input):
    candidate_labels = list(df['University_name'].unique())
    nlp_result = nlp(user_input, candidate_labels)
    best_label = nlp_result['labels'][0]
    
    university_info = df[df['University_name'].str.contains(best_label, case=False, na=False)]
    if not university_info.empty:
        info = university_info.iloc[0]
        return f"The minimum IELTS score required for {info['University_name']} is {info['Minimum_IELTS_score']}."
    else:
        return "No matching universities found."

# Function to get information about international students
def get_international_students_info(user_input):
    candidate_labels = list(df['University_name'].unique())
    nlp_result = nlp(user_input, candidate_labels)
    best_label = nlp_result['labels'][0]
    
    university_info = df[df['University_name'].str.contains(best_label, case=False, na=False)]
    if not university_info.empty:
        info = university_info.iloc[0]
        return f"{info['University_name']} has {info['International_students']} international students."
    else:
        return "No matching universities found."

if __name__ == '__main__':
    app.run(debug=True)
