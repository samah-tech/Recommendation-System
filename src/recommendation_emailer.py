from preprocessing import load_and_preprocess_data
from recommender import generate_recommendations
from email_utils import generate_messages, send_email
import pandas as pd

def main():
    # Preprocess data (saves CSVs and returns full df)
    df_cleaned = load_and_preprocess_data()
    print(df_cleaned.shape)
    # Generate recommendations (returns df)
    df_recommendations = generate_recommendations(df_cleaned)
    print (df_recommendations.shape)
    
    # Generate email and WhatsApp messages for each row
    df_recommendations[['email_message', 'whatsapp_message']] = df_recommendations.apply(generate_messages, axis=1, result_type='expand')
    print (df_recommendations.shape)
    # Send emails to each user (loop over rows)
    for _, row in df_recommendations.tail(4).iterrows():
        send_email(row['email'], row['email_message'])
    #send_email(df_recommendations.iloc[-1]['email'], df_recommendations.iloc[-1]['email_message'])

if __name__ == "__main__":
    main()