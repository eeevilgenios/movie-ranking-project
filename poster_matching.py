import csv

def main():
    posters = {}
    with open("posters.csv","r") as f:
        reader = csv.reader(f)
        for row in reader:
            movie = row[1]
            url = row[14]
            if not url:
                continue
            posters[movie] = url
    
    with open("unsorted.txt", "r") as f:
        for movie in f.readlines():
            movie = movie.strip()
            url = posters.get(movie)
            if url is None:
                print(movie)
            else:
                print(movie, url)

if __name__ == "__main__":
    main()