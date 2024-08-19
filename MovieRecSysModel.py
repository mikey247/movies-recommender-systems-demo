import pandas as pd                          
from surprise import Dataset, Reader, SVD         
from surprise.model_selection import cross_validate   
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load data

movies = pd.read_csv('./ml-latest-small/movies.csv')
ratings = pd.read_csv('./ml-latest-small/ratings.csv')
links = pd.read_csv('./ml-latest-small/links.csv')

# movies = pd.read_csv('./ml-25m/movies.csv')

# ratings = pd.read_csv('./ml-25m/ratings.csv')

# links = pd.read_csv('./ml-25m/links.csv')


# Create an instance of the Reader class, defining the rating range as 0.5 to 5 
reader = Reader(rating_scale=(0.5, 5))

# Load the data from the ratings dataframe and create a Dataset object,
# passing the user id, movie id and rating columns as input to the load_from_df() method
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)




###
### Convert the 'tmdbId' to integer and drop rows with missing values
links = links.dropna(subset=['tmdbId'])
links['tmdbId'] = links['tmdbId'].astype(int)

# Merge the MovieLens and TMDB datasets using 'movieId' column
movies = movies.merge(links, left_on='movieId', right_on='movieId')

# Merge the movies dataset with the ratings dataset
movies_with_ratings = movies.merge(ratings, on='movieId')




# Create an object of the SVD algorithm.
svd = SVD()

# Use the cross_validate function to apply K-fold cross-validation on the data for the svd model.
# Here, 5-fold cross-validation is used.
# The evaluation metrics used are RMSE(Root Mean Squared Error) and MAE(Mean Absolute Error).
# verbose parameter is set to True to show more details during cross-validation.
cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)


# Instantiate a TfidfVectorizer object with 'english' stop words
# This will help us remove common English words such as 'the', 'and', etc., from the text data
tfidf = TfidfVectorizer(stop_words='english')

# Replace missing genre values with an empty string
movies['genres'] = movies['genres'].fillna('')

# Fit the TfidfVectorizer to the 'genres' column of the movies DataFrame, transforming the text data into a numerical format
# This generates a sparse matrix of TF-IDF values for each genre in the dataset
tfidf_matrix = tfidf.fit_transform(movies['genres'])

# Compute the cosine similarity between each pair of movies using their corresponding TF-IDF vectors
# This will give us a measure of how similar the movies are based on their genres
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)



# Create a pandas Series with movie titles as the index and their corresponding DataFrame index as values
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Define a function for generating content-based recommendations
def content_based_recommendations(title, n=10):
    # Obtain the index of the movie that matches the provided title
    index = indices[title]
    
    # Create a list of tuples containing the index and cosine similarity score for each movie
    sim_scores = list(enumerate(cosine_sim[index]))
    
    # Sort the list of similarity scores in descending order, so the highest scores come first
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Select the top 'n' highest scoring movies, excluding the first one (itself)
    sim_scores = sim_scores[1:n+1]
    
    # Extract the indices of the selected movies
    movie_indices = [i[0] for i in sim_scores]
    
    # Return the titles of the selected movies using their indices
    return movies['title'].iloc[movie_indices]




# Define a hybrid recommendation function that combines content-based and collaborative filtering approaches
def hybrid_recommendations(user_id=1, title="", n=10):
    # Obtain content-based recommendations for the given title and convert them to a DataFrame
    content_based = content_based_recommendations(title, n).to_frame()
    content_based.columns = ['title']
    
    # Merge the content-based recommendations with the movies_with_ratings DataFrame on the 'title' column
    content_based = content_based.merge(movies_with_ratings, on='title')
    
    # Remove duplicate movies, keeping only the first occurrence
    content_based = content_based.drop_duplicates(subset=['title'], keep='first')
    
    # Calculate the estimated rating for each recommended movie using the SVD model and the provided user_id
    content_based['est'] = content_based['movieId'].apply(lambda x: svd.predict(user_id, x).est)
    
    # Sort the movies by their estimated ratings in descending order
    content_based = content_based.sort_values('est', ascending=False)
    
    # Return the top 'n' movie titles with the highest estimated ratings
    return content_based.head(n)['title']

def get_all_movies():
    # get all movie titles and their imdb id 
    return movies[['title', 'imdbId']].to_dict(orient='records')

# # Define the user ID, movie title, and the number of recommendations to generate
# user_id = 2 # User ID for which recommendations will be generated
# title = 'Toy Story (1995)' # Movie title based on which recommendations will be generated
# n = 10

# # Call the hybrid_recommendations function to generate 'n' recommendations for the user based on the provided movie title
# recommendations = hybrid_recommendations(user_id, title, n)

# # Convert the recommendations to a list
# recommendations_list = recommendations.tolist()

# # Print the top 'n' recommendations for the user, showing which movie they are based on
# print(f"Top {n} recommendations for User {user_id} who likes '{title}':")

# # Iterate through the recommendations list and print each movie title with its corresponding rank
# for i, movie_title in enumerate(recommendations_list, start=1):
#     print(f"{i}. {movie_title}")