# Recommendation Emailer

This project sends automated recommendations via email.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your email password as an environment variable:
   ```bash
   export EMAIL_PASS=your_app_password
   ```

3. Run the script:
   ```bash
   python recommendation_emailer.py
   ```

## Deployment

To automate, deploy with a cron job or a cloud service like PythonAnywhere.

## Files

- `preprocessing.py` – Loads and cleans data
- `recommender.py` – Generates top-N recommendations
- `email_utils.py` – Builds and sends email
- `config.py` – Stores static config like sender/receiver
