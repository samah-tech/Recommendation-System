import os
import warnings
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

# Suppress warnings and TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

def generate_recommendations(df_cleaned, model_path='all-MiniLM-L6-v2'):
    """
    Generate course recommendations for users based on their specialization and webinar data.
    
    Args:
        df_cleaned (pd.DataFrame): Preprocessed customer data with 'specialization', 'webinar', 'email', 'full_name', 'phone'.
        model_path (str): Path to SentenceTransformer model (default: 'all-MiniLM-L6-v2' or local path).
    
    Returns:
        pd.DataFrame: DataFrame with recommendations (name, email, webinar_name, whatsapp_number, course_1_name, course_1_link, etc.).
    """
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    courses_data_preprocessed = os.path.join(base_dir, "..", "data", "processed_courses_data.csv")
    output_path_recommendations = os.path.join(base_dir, "..", "data", "recommendations.csv")

    # Load courses data
    courses_df = pd.read_csv(courses_data_preprocessed)

    # Set device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load model
    try:
        model = SentenceTransformer(model_path, device=device)
    except Exception as e:
        print(f"Error loading model: {e}. Ensure internet connection or use a local model path.")
        raise

    # Combine text for embeddings
    df_cleaned['user_text'] = df_cleaned['specialization'] + " " + df_cleaned['webinar']
    courses_df['course_text'] = (
        courses_df['course_title'] + " " +
        courses_df['Course classification'] + " " +
        courses_df['type']
    )

    # Generate embeddings
    user_embeddings = model.encode(df_cleaned['user_text'].tolist(), convert_to_tensor=True)
    course_embeddings = model.encode(courses_df['course_text'].tolist(), convert_to_tensor=True)

    # Compute cosine similarities
    cosine_scores = util.cos_sim(user_embeddings, course_embeddings)

    top_n = 3  # Number of recommendations per user
    recommendations = []

    for user_idx, row in enumerate(df_cleaned.itertuples(index=False)):
        user_email = row.email
        user_name = row.full_name
        user_phone = row.phone
        user_webinar = row.webinar
        top_indices = cosine_scores[user_idx].cpu().numpy().argsort()[-top_n:][::-1]

        # Get course titles and links
        recommended_courses_data = courses_df.iloc[top_indices][['course_title', 'Course_link']].to_dict(orient='records')
        formatted_recommended_courses = [
            {'course_name': c['course_title'], 'course_link': c['Course_link']}
            for c in recommended_courses_data
        ]

        recommendations.append({
            'name': user_name,
            'webinar_name': user_webinar,
            'email': user_email,
            'whatsapp_number': user_phone,
            'recommended_courses': formatted_recommended_courses
        })

    df_recommendations = pd.DataFrame(recommendations)

    # Flatten structure
    for i in range(top_n):
        df_recommendations[f'course_{i+1}_name'] = df_recommendations['recommended_courses'].apply(
            lambda x: x[i]['course_name'] if len(x) > i else None
        )
        df_recommendations[f'course_{i+1}_link'] = df_recommendations['recommended_courses'].apply(
            lambda x: x[i]['course_link'] if len(x) > i else None
        )

    df_recommendations.drop(columns=['recommended_courses'], inplace=True)
    df_recommendations.to_csv(output_path_recommendations, index=False)

    return df_recommendations

# if __name__ == "__main__":
#     # For standalone testing
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     customer_data_preprocessed = os.path.join(base_dir, "..", "data", "processed_customer_data.csv")
#     df_cleaned = pd.read_csv(customer_data_preprocessed)
#     rec = generate_recommendations(df_cleaned)
#     print(rec.shape)