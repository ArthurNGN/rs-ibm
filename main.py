from process_data_source import process_film_registry
from setup_logging import setup_logging
from plot_to_triples_multi_threading_v2 import process_movie_df
from process_triples import process_triples_df
import pandas as pd

def main():
    # affichage des messages
    setup_logging()

    # pathing
    root_path = '/Users/nguyen/Desktop/RS'
    data_source_folder = root_path+'/data_source/'
    results_folder = root_path+'/results/'

    # load tmdb df and std
    tmdb_cols = {
            'id': 'movie_id',
            'original_title': 'title',
            'overview': 'plot'
        }
    df_tmdb = process_film_registry([data_source_folder+'tmdb_5000_movies.csv'], tmdb_cols, results_folder+"df_tmdb.csv")

    # load grouplens df and std
    # in ratings    : userId,movieId,rating,timestamp
    # in movies     : movieId,title,genres
    # in links      : movieId,imdbId,tmdbId
    gl_cols = {
            'movieId': 'movie_id',
            'title': 'title',
            'userId': 'user_id',
            'rating': 'rating',
            'genres': 'genres',
            'imdbId': 'imdb_movie_id',
            'tmdbId': 'tmdb_movie_id'
        }
    df_gl = process_film_registry([data_source_folder+'ml-latest-small/ratings.csv',
                                   data_source_folder+'ml-latest-small/movies.csv',
                                   data_source_folder+'ml-latest-small/links.csv'],
                                   gl_cols, results_folder+"df_gl.csv")

    # working subset
    df_tmdb_subset = df_tmdb.head(16)

    # create triples (avoid building a df)
    process_movie_df(df_tmdb_subset, 5, results_folder+"film_registry_triples.csv")

    # load csv triples
    df_film_registrey_triples = pd.read_csv(results_folder+"film_registry_triples.csv")

    # process triples
    df_processed_film_registrey_triples = process_triples_df(df_film_registrey_triples, results_folder+"film_registry_processed_triples.csv")

if __name__ == "__main__":
    main()
