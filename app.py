import requests
from bs4 import BeautifulSoup
import streamlit as st

# Setting some text input variables for calling the initial Yelp API requests
latitude = st.text_input('Latitude', '33.0171914')
longitude = st.text_input('Longitude', '-117.1261851')
term = st.text_input('What type of establihment are you looking for?', 'restaurant')
# categories = st.text_input('What type of food?', 'Mexican')
price = st.number_input('How expensive of an establishemnt?', min_value=1, max_value=4)
open_now = st.text_input('Open or closed?', 'True')

# debugging
# latitude = '33.0171914'
# longitude = '-117.1261851'
# term = 'restaurant'
# price = 3
# open_now = 'True'

business_search_url = f"https://api.yelp.com/v3/businesses/search?latitude={latitude}&longitude={longitude}&term={term}&categories=&price={price}&open_now={open_now}&sort_by=best_match&limit=10"

business_search_headers = {
    "accept": "application/json",
    "Authorization": "Bearer 9CCFyEWk3fKd3CPFMjtkRX3ja4jecUFGfjvWPTbn1uIvB_Zr5VHqP8nKthjmoDBzuSRYNY_7OFaoSwOQJ22aNhfewTHgo1eNSrrhja4SG1c105V8pfeI6Es2J8yXY3Yx"
}

business_search_response = requests.get(business_search_url, headers=business_search_headers)

# get business ID as a variable to search and get their reviews
business_ids = []
business_names = []
business_search_json = business_search_response.json()
for business in business_search_json['businesses']:
    business_ids.append(business['id'])
    business_names.append(business['name'])

st.header('Top 10 Restaurants in the area')
st.write(business_names)

# Collection of reviews from business 
reviewers_id = []
for biz_id in business_ids:
    business_reviews_url = f"https://api.yelp.com/v3/businesses/{biz_id}/reviews?limit=50&sort_by=yelp_sort"

    business_reviews_headers = {
        "accept": "application/json",
        "Authorization": "Bearer 9CCFyEWk3fKd3CPFMjtkRX3ja4jecUFGfjvWPTbn1uIvB_Zr5VHqP8nKthjmoDBzuSRYNY_7OFaoSwOQJ22aNhfewTHgo1eNSrrhja4SG1c105V8pfeI6Es2J8yXY3Yx"
    }

    business_reviews_response = requests.get(business_reviews_url, headers=business_reviews_headers)
    business_reviews_json = business_reviews_response.json()

    for review in business_reviews_json['reviews']:
        reviewers_id.append(review)

reviewer_stats = []
# Search for user and determine their influence & impact
for reviewer in reviewers_id:
    user_id = reviewer['user']['id']
    reviewer_url = f"https://www.yelp.com/user_details?userid={user_id}"

    reviewer_headers = {
        "accept": "application/json",
    }

    reviewer_response = requests.get(reviewer_url, headers=reviewer_headers)

    reviewer_soup = BeautifulSoup(reviewer_response.text, 'html.parser')
    reviewer_results = reviewer_soup.findAll(class_='user-details-overview_sidebar')

    # Loop through review-content divs and extract paragraph text
    for reviewer_result in reviewer_results:
        reviewer_stats.append(reviewer_result.find_all('div'))

user_list= []
for rating in reviewer_stats:
    if len(rating) < 5:
        pass
    else:
        user_list.append(rating[4])

user_ranking = []
for user_item in user_list:
    if user_item.attrs == {'class': ['histogram_bar']}:
        pass
    else:
        user_ranking.append(user_item)

tmp = []
for user_item in user_ranking:
    if user_item.attrs == {'class': ['ysection']}:
        tmp.append(user_item.contents)

for item in tmp:
    if len(item) > 3:
        st.write(item[3].text)
        st.write('------------')