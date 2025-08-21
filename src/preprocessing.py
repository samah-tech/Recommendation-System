import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

def load_and_preprocess_data():
    # Get path to current file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go to the `data` folder at the root of the repo
    course_path = os.path.join(base_dir, "..", "data", "courses.xlsx")
    customer_path = os.path.join(base_dir, "..", "data", "customer_data.xlsx")

    #output_path
    output_path_customer = os.path.join(base_dir, "..", "data", "processed_customer_data.csv")
    output_path_courses = os.path.join(base_dir, "..", "data", "processed_courses_data.csv")


    customer_df = pd.read_excel(customer_path)
    courses_df = pd.read_excel(course_path)
    #print (courses_df.head())

    # Check if 'Unnamed: 0' column exists and drop it
    if 'unnamed_cols' in customer_df.columns:
        customer_data = customer_df.drop(columns=['unnamed_cols'])
    else:
        pass
        #print (courses_df.head())

        #for courses
    courses_df.rename(columns={'رابط الكورس':'Course_link','Course':'course_title'},inplace = True)
    #for customers
    df_cleaned = customer_df[[
        'اسم الورشة',
        'Email Address',
        'رقم الهاتف المحمول',
        'الاسم الكامل',
        'دولة الإقامة',
        'ماهو تخصصك العلمي ومجالك الوظيفي؟',
        'Timestamp'
    ]]
    df_cleaned.rename(columns={
        'اسم الورشة': 'webinar',
        'Email Address': 'email',
        'رقم الهاتف المحمول':'phone',
        'الاسم الكامل': 'full_name',
        'دولة الإقامة': 'country',
        'ماهو تخصصك العلمي ومجالك الوظيفي؟': 'specialization',
        'Timestamp': 'timestamp'
    },inplace=True)
    # Clean text fields: strip spaces and lowercase
    # df_cleaned['webinar'] = df_cleaned['webinar'].str.strip().str.lower()
    # df_cleaned['specialization'] = df_cleaned['specialization'].str.strip().str.lower()
    # df_cleaned['country'] = df_cleaned['country'].str.strip().str.lower()
    # df_cleaned['full_name'] = df_cleaned['full_name'].str.strip()

    # Drop rows with missing critical fields
    df_cleaned = df_cleaned.dropna(subset=['email', 'webinar', 'specialization'])
    # Save cleaned data to CSV
    df_cleaned.to_csv(output_path_customer, index=False)
    courses_df.to_csv(output_path_courses, index=False)
    return  df_cleaned

#load_and_preprocess_data()
