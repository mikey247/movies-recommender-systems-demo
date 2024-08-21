
# Define the user ID, movie title, and the number of recommendations to generate
user_id = 2 # User ID for which recommendations will be generated
title = 'Toy Story (1995)' # Movie title based on which recommendations will be generated
n = 10

# Call the hybrid_recommendations function to generate 'n' recommendations for the user based on the provided movie title
recommendations = hybrid_recommendations(user_id, title, n)

# Convert the recommendations to a list
recommendations_list = recommendations.tolist()

# Print the top 'n' recommendations for the user, showing which movie they are based on
print(f"Top {n} recommendations for User {user_id} who likes '{title}':")

# Iterate through the recommendations list and print each movie title with its corresponding rank
for i, movie_title in enumerate(recommendations_list, start=1):
    print(f"{i}. {movie_title}")