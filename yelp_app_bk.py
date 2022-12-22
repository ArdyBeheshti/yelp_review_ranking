import requests
from bs4 import BeautifulSoup
import streamlit as st
import os
from geopy.geocoders import Nominatim
import json
import pandas as pd

geolocator = Nominatim(timeout=None, user_agent = "tmpGeo")

# pull files from api or local?
# st.file_uploader()
# os.chdir(r'C:\Users\ardyb\OneDrive\Desktop\yelp_review_ranking\test_data')

price = []
# Setting some text input variables for calling the initial Yelp API requests
with st.sidebar:
    # debugging
    zip_code = 92128
    term = 'restaurant'
    price = 3
    zip_code = st.text_input('Please enter your ZIP code')
    if zip_code:
        location = geolocator.geocode(zip_code)
        latitude = location.latitude
        longitude = location.longitude
    term = st.text_input('What type of establihment are you looking for?', 'restaurant')
    # categories = st.text_input('What type of food?', 'Mexican')
    price = st.selectbox('How expensive of an establishemnt?', ['💲', '💲💲', '💲💲💲', '💲💲💲💲'])

    if price == '💲':
        price = 1
    elif price == '💲💲':
        price = 2
    elif price == '💲💲💲':
        price = 3
    else:
        price = 4

if zip_code and term and price:
    business_search_url = f"https://api.yelp.com/v3/businesses/search?latitude={latitude}&longitude={longitude}&term={term}&categories=&price={price}&open_now=True&sort_by=best_match&limit=50"

    business_search_headers = {
        "accept": "application/json",
        "Authorization": "Bearer 9CCFyEWk3fKd3CPFMjtkRX3ja4jecUFGfjvWPTbn1uIvB_Zr5VHqP8nKthjmoDBzuSRYNY_7OFaoSwOQJ22aNhfewTHgo1eNSrrhja4SG1c105V8pfeI6Es2J8yXY3Yx"
    }

    business_search_response = requests.get(business_search_url, headers=business_search_headers)
    business_search_parse = json.loads(business_search_response.text)
    inner_parse_business_search = business_search_parse['businesses']
    business_df = pd.DataFrame.from_dict(pd.json_normalize(inner_parse_business_search), orient='columns')

    # # get business ID as a variable to search and get their reviews
    # business_ids = []
    # business_names = []
    # business_addr = []
    # business_search_json = business_search_response.json()
    # # st.write(business_search_json)
    # for business in business_search_json['businesses']:
    #     business_ids.append(business['id'])
    #     business_names.append(business['name'])
    #     business_addr.append(business['location']['display_address'])

    # Collection of reviews from business 
    reviews = []
    for biz_id in business_df['id']:
        business_reviews_url = f"https://api.yelp.com/v3/businesses/{biz_id}/reviews?limit=50&sort_by=yelp_sort"

        business_reviews_headers = {
            "accept": "application/json",
            "Authorization": "Bearer 9CCFyEWk3fKd3CPFMjtkRX3ja4jecUFGfjvWPTbn1uIvB_Zr5VHqP8nKthjmoDBzuSRYNY_7OFaoSwOQJ22aNhfewTHgo1eNSrrhja4SG1c105V8pfeI6Es2J8yXY3Yx"
        }

        business_reviews_response = requests.get(business_reviews_url, headers=business_reviews_headers)
        # business_reviews_json = business_reviews_response.json()
        # for review in business_reviews_json['reviews']:
        #     reviewers_id.append(review)

        business_reviews_parse = json.loads(business_reviews_response.text)
        inner_parse_business_review = business_reviews_parse['reviews']
        review_tmp_df = pd.DataFrame.from_dict(pd.json_normalize(inner_parse_business_review), orient='columns')
        reviews.append(review_tmp_df)
    
    reviews_df = pd.concat(reviews)

    st.dataframe(business_df)
    # st.dataframe(reviews_df)

    if business_df['rating']:
        st.write('nothere')

    top_ten = business_df[business_df['rating'] == 4.5].nlargest(10, 'review_count')['name']
    top_address = business_df[business_df['rating'] == 4.5].nlargest(10, 'review_count')['location.address1']

    # rest_col, addr_col, rev_col = st.columns(3)

    # st.header('Find the top Restaurants in your area!')
    # with rest_col:
    #     st.write(business_names)

    # with addr_col:
    #     st.write(business_addr)

    # with rev_col:
    #     st.write(reviewers_id[0])

    # reviewer_stats = []
    # # Search for user and determine their influence & impact
    # for reviewer in reviewers_id:
    #     user_id = reviewer['user']['id']
    #     reviewer_url = f"https://www.yelp.com/user_details?userid={user_id}"

    #     reviewer_headers = {
    #         "accept": "application/json",
    #     }

    #     reviewer_response = requests.get(reviewer_url, headers=reviewer_headers)

    #     reviewer_soup = BeautifulSoup(reviewer_response.text, 'html.parser')
    #     reviewer_results = reviewer_soup.findAll(class_='user-details-overview_sidebar')

    #     # Loop through review-content divs and extract paragraph text
    #     for reviewer_result in reviewer_results:
    #         reviewer_stats.append(reviewer_result.find_all('div'))

    # user_list= []
    # for rating in reviewer_stats:
    #     if len(rating) < 5:
    #         pass
    #     else:
    #         user_list.append(rating[4])

    # user_ranking = []
    # for user_item in user_list:
    #     if user_item.attrs == {'class': ['histogram_bar']}:
    #         pass
    #     else:
    #         user_ranking.append(user_item)

    # tmp = []
    # for user_item in user_ranking:
    #     if user_item.attrs == {'class': ['ysection']}:
    #         tmp.append(user_item.contents)

    # for item in tmp:
    #     if len(item) > 3:
    #         st.write(item[3].text)
    #         st.write('------------')