import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor 
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score
import pickle
from datetime import datetime, date
import time
import streamlit as st
import itertools

# pull files from api or local?
# st.file_uploader()
os.chdir(r'C:\Users\ardyb\OneDrive\Desktop\yelp_review_ranking\test_data')

# Business data import
business_json_path = 'yelp_academic_dataset_business.json'
business = pd.read_json(business_json_path, lines=True)

with st.sidebar:
    # let user select location by zipcode
    postal_code = st.selectbox('Please select a ZIP code', (business['postal_code']))

    # Keep only operating buisnesses and remove non-relevant columns
    df_business = business[business['is_open']==1].drop(['is_open','review_count'], axis=1)
    df_business = business[business['postal_code']==postal_code]

    # %timeit set(itertools.chain.from_iterable(df.Genre))
    df_explode = df_business.assign(categories = df_business.categories.str.split(', ')).explode('categories')
    unique_categories = df_explode['categories'].explode().unique()
    
    # let user select category of business
    category = st.selectbox('Pick a category', (unique_categories))

if postal_code and category:
    # Top restaurants
    # Only businesses that include restarants categorization
    business_restaurants = df_explode[df_explode.categories==category]

    st.header(f'Find the top {category} in your area!')

    # display 10 top restaurants
    # display top users and their review
    top_ten = business_restaurants[business_restaurants['stars'] == 5.0].nlargest(10, 'review_count')['name']
    top_address = business_restaurants[business_restaurants['stars'] == 5.0].nlargest(10, 'review_count')['address']

    # # Load review data, work with chunksize to avoid RAM problems
    # review_json_path = 'yelp_academic_dataset_review.json'
    # review = pd.read_json(review_json_path, lines=True,
    #                       # Identification of data types can reduce RAM consumption
    #                       dtype={'review_id':str,'user_id':str,'business_id':str,'stars':int,
    #                              'date':str,'text':str,'useful':int,'funny':int,'cool':int},
    #                       chunksize=1000000)

    # # Join review data using the business_ids from restaurants
    # chunk_list = []
    # for chunk in review:
    #     # Rename columns to avoid conflicts
    #     chunk = chunk.rename(columns={'stars': 'review_stars', 'useful': 'review_useful', 'funny': 'review_funny', 'cool': 'review_cool', 'text': 'review_text', 'date': 'review_date'})
    #     chunk_merged = pd.merge(business_restaurants, chunk, on='business_id', how='inner')
    #     chunk_list.append(chunk_merged)

    # # Chunks merge
    # df_restaurant_review = pd.concat(chunk_list, ignore_index=True, join='outer', axis=0)

    # # Load user data, work with chunksize to avoid RAM problems
    # user_json_path = 'yelp_academic_dataset_user.json'
    # user = pd.read_json(user_json_path, lines=True, 
    #                     dtype={'user_id':str,'name':str,'review_count':int,
    #                            'yelping_since':str,'useful':int,'funny':int,'cool':int,'elite':str,'friends':str,
    #                            'fans':int,'average_stars':float,'compliment_hot':int,'compliment_more':int,'compliment_profile':int,
    #                            'compliment_cute':int,'compliment_list':int,'compliment_note':int,'compliment_plain':int,
    #                            'compliment_cool':int,'compliment_funny':int,'compliment_writer':int,'compliment_photos':int},
    #                     chunksize=100000)


    # # Join user data using the relevant user_ids
    # chunk_list_user = []
    # for chunk in user:
    #     # Rename columns to avoid conflicts
    #     chunk = chunk.rename(columns={'name': 'user_name', 'useful': 'user_useful', 'funny': 'user_funny', 'cool': 'user_cool', 'elite': 'user_elite', 'fans': 'user_fans', 'average_stars': 'user_average_stars', 'friends': 'user_friends', 'review_count': 'user_review_count', 'yelping_since': 'user_yelping_since'})
    #     chunk_merged_user = pd.merge(df_restaurant_review, chunk, on='user_id', how='inner') 
    #     chunk_list_user.append(chunk_merged_user)


    # # Chunks merge
    # df_full = pd.concat(chunk_list_user, ignore_index=True, join='outer', axis=0)

    # # Convert a user's friend list into a count
    # df_full['user_friends_count'] = df_full.user_friends.apply(lambda x: '0' if x == 'None' else len(x.split(',')))
    # df_full = df_full.drop(['user_friends'], axis=1)

    # # Convert individual user's elite awards into a count
    # df_full['user_elite_count'] = df_full.user_elite.apply(lambda x: '0' if x == '' else len(x.split(',')))
    # df_full = df_full.drop(['user_elite'], axis=1)

    # # Convert the date of user account creation to the age of the account in days
    # df_full["user_yelping_since"] = pd.to_datetime(df_full["user_yelping_since"])
    # df_full["user_yelping_since"] = df_full["user_yelping_since"].dt.date
    # df_full['user_age'] = (date.today() - df_full['user_yelping_since']).dt.days
    # df_full = df_full.drop(['user_yelping_since'], axis=1)

    # top_review = df_full[df_full['stars'] == 5.0].nlargest(10, 'review_count')['user_review']

    rest_col, addr_col, rev_col = st.columns(3)
    
    with rest_col:
        st.write(top_ten)

    with addr_col:
        st.write(top_address)

    # with rev_col:
    #     st.write(top_review)









# # df_sample = df_full.sample(100000)

# # Definition of attributes/features by removing all non-relevant columns for the model
# X = df_full.drop(['stars', 'business_id', 'name', 'address', 'city', 'state', 'postal_code', 'latitude', 
#                    'longitude', 'attributes', 'categories', 'hours', 'review_id', 'review_text', 'review_date', 
#                    'user_id', 'user_name', 'review_stars', 'review_useful', 'review_funny', 'review_cool'], axis=1) 
# # Definition of label/target
# y = df_full['stars']

# # Split the data into train and test data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# # Create and fit regressor
# regressor = DecisionTreeRegressor(random_state = 0) 
# regressor.fit(X, y)

# # Predict with test Create data and compare it with actual values
# y_pred = regressor.predict(X_test)
# actual_prediction=pd.DataFrame({'Actual':y_test, 'Predicted':y_pred})
# actual_prediction.sample(10)

# time.sleep(120)

# # Create metrics for predictions
# print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
# print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
# print('R2 Score:', r2_score(y_test, y_pred))
# print('Cross Validation Score:', cross_val_score(regressor, X, y, cv=5).mean())

# # Export Model
# filename = 'yelp_model.pkl'
# pickle.dump(regressor, open(filename, 'wb'))

# df_sample.to_csv("yelp_sample.csv", index=False)