import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self):
        # -----------------------------
        # Sample Movie Ratings Dataset
        # -----------------------------
        data = {
            "user_id": [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5],
            "movie": [
                "Inception","Avengers","Titanic","Interstellar",
                "Inception","Avengers","Titanic","Interstellar",
                "Inception","Avengers","Titanic","Interstellar",
                "Inception","Avengers","Titanic","Interstellar",
                "Inception","Avengers","Titanic","Interstellar"
            ],
            "rating": [
                5,4,2,5,
                4,5,1,4,
                1,2,5,2,
                5,4,2,5,
                2,1,5,2
            ]
        }

        self.df = pd.DataFrame(data)

        # Create User-Movie Matrix
        self.user_movie_matrix = self.df.pivot_table(
            index="user_id",
            columns="movie",
            values="rating"
        ).fillna(0)

        # Compute Similarity Matrix
        self.similarity_matrix = cosine_similarity(self.user_movie_matrix)

        self.similarity_df = pd.DataFrame(
            self.similarity_matrix,
            index=self.user_movie_matrix.index,
            columns=self.user_movie_matrix.index
        )

    def recommend_movies(self, user_id, top_n=3):

        if user_id not in self.user_movie_matrix.index:
            print("Invalid User ID")
            return []

        # Step 1: Get similarity scores
        similarity_scores = self.similarity_df[user_id].drop(user_id)

        # Step 2: Weighted rating calculation
        weighted_ratings = np.zeros(len(self.user_movie_matrix.columns))

        for other_user, similarity in similarity_scores.items():
            other_user_ratings = self.user_movie_matrix.loc[other_user].values
            weighted_ratings += similarity * other_user_ratings

        # Step 3: Remove already watched movies
        user_ratings = self.user_movie_matrix.loc[user_id].values
        weighted_ratings[user_ratings > 0] = 0

        # Step 4: Create recommendation list
        recommendation_scores = pd.Series(
            weighted_ratings,
            index=self.user_movie_matrix.columns
        )

        recommended_movies = recommendation_scores.sort_values(
            ascending=False
        ).head(top_n)

        return recommended_movies


# -----------------------------
# Run the System
# -----------------------------
if __name__ == "__main__":

    recommender = MovieRecommender()

    print("\n===== Movie Recommendation System =====")
    print("Available Users: 1, 2, 3, 4, 5")

    try:
        user_id = int(input("Enter User ID: "))
        recommendations = recommender.recommend_movies(user_id)

        if len(recommendations) == 0:
            print("No recommendations available.")
        else:
            print("\nTop Recommended Movies:\n")
            for movie, score in recommendations.items():
                print(f"{movie}  | Predicted Score: {round(score,2)}")

    except ValueError:
        print("Please enter a valid numeric User ID.")
