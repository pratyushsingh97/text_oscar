import csv

def reviews(movie_title):
    with open('resources/movies_final.csv', newline='') as movies_list:
        reader = csv.DictReader(movies_list)
        review = None
        
        try:
            review = next(row['review_summary'] for row in reader if row['movie_title'] == movie_title)
        
        # TODO: LOG and then we would have an engine that would go and retrieve the reviews
        except:
            print("Movie review not available")
            
        
        movies_list.close()
        
        return review