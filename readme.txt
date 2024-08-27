# University Recommendation ChatBot

A university recommendation chatbot built using Rasa for Natural Language Understanding (NLU) and Flask for the backend API. This chatbot assists students in finding universities based on various criteria like ranking, location, and tuition fees.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Overview

This chatbot leverages machine learning to understand user queries and provides university recommendations. The system uses BERT-based models for intent recognition and entity extraction. The backend is implemented using Flask, which handles API requests and integrates the Rasa bot.

## Features

- **Natural Language Understanding**: Understands user queries using Rasa NLU and BERT models.
- **Custom Actions**: Performs custom actions like fetching university rankings, locations, and fees.
- **Integration with Flask**: Backend API developed using Flask to manage user sessions and integrate Rasa.
- **Machine Learning Models**: Uses pre-trained models for token classification to improve response accuracy.

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtual environment (optional but recommended)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/UniversityRecommendationChatBot.git
   cd UniversityRecommendationChatBot

Commands
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt

rasa train

rasa run --enable-api

rasa run actions

rasa run



