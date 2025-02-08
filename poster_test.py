import csv

unsorted_movies = {}

with open("unsorted.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            movie = row[0]
            url = row[1]
            if not url:
                continue
            unsorted_movies[movie] = url

print(unsorted_movies)