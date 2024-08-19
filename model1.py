import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
movies = pd.read_csv('./ml-latest-small/movies.csv')
ratings = pd.read_csv('./ml-latest-small/ratings.csv')

# movies = pd.read_csv("./ml-25m/movies.csv")
# ratings = pd.read_csv("./ml-25m/ratings.csv")

def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", '', title)
    title = title.strip()
    return title

movies['clean_title'] = movies['title'].apply(clean_title) # apply function to each row
movies['clean_title'] = movies['clean_title'].str.lower()

# Create a TfidfVectorizer to convert words into vectors
vectorizer =  TfidfVectorizer(ngram_range=(1, 2))

# Fit the vectorizer to the data, to turn our set of titles into a matrix of numbers
tfdif = vectorizer.fit_transform(movies['clean_title'])

# print(tfdif)

def search_movie(search_term):
    # Clean the search term
    search_term = clean_title(search_term)

    # Convert the search term into a vector
    search_vec = vectorizer.transform([search_term])

    # Calculate the cosine similarity between the search term and all the titles
    similarity = cosine_similarity(search_vec, tfdif).flatten()

    # Find the indices of the top 5 most similar movies
    indices = np.argpartition(similarity, -5)[-5:]

    # Retrieve the top 5 most similar movies based on the indices
    results = movies.iloc[indices][::-1]# reverse the order because the most similar movie has the highest cosine similarity and is at the end of the list currently

    return results

# print(movies)
# print(ratings)

# search_term = input("Enter a movie title: ")
# print(search_movie(search_term))

def find_similar_users(movie_id):
    # Get all the ratings for that particular movie
    movie_ratings = ratings[ratings['movieId'] == movie_id]
    
    # Get all the users that rated the movie
    users = movie_ratings['userId'].unique()

    # Get ratings of more than 4
    users = users[movie_ratings['rating'] > 4]

    return users


def get_similar_user_recs(similar_users):
    # Get all the ratings of the similar users and filter out ratings less than 4
    similar_user_recs = ratings[(ratings['userId'].isin(similar_users)) & (ratings['rating'] > 4)]["movieId"]
    return similar_user_recs

similar_users = find_similar_users(1)
similar_user_recs = get_similar_user_recs(similar_users)

# get the count of each movie and divide by the total number of similar users to get the percentage of similar users that rated that movie
similar_user_recs = similar_user_recs.value_counts()/len(similar_users)
# filter out movies that have less than 10% of similar users that rated it
similar_user_recs = similar_user_recs[similar_user_recs > 0.1]
print(similar_user_recs)