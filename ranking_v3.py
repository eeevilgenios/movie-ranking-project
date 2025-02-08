def save(unsorted_movies):
    with open("unsorted.txt", "w") as f:
        for i in unsorted_movies:
            print (i)
            f.write(str(i))
            f.write("\n")

def sort(movie, sorted_movies, in_recursive):
    if len(sorted_movies) == 0:
        sorted_movies.append(str(movie))
        return(sorted_movies)
    if len(sorted_movies) == 1:
        while True:
            choice = input("Enter 1 or 2: ").strip()
            if choice in ["1", "2"]:
                break
            print("Invalid input. Please enter 1, 2.")
        

    print(f"Which movie do you prefer? (1: {movie}, 2: {pivot})")
    while True:
        choice = input("Enter 1 or 2 (or 'undo', 'save', 'quit'): ").strip()
        if choice in ["1", "2", "undo", "save", "quit"]:
            break
        print("Invalid input. Please enter 1, 2, 'undo', 'save', or 'quit'.")
    
    if choice == "save":
        save_progress(movies, comparison_cache, "progress.json")
        print(f"\nTotal comparisons made: {comparison_count}")
        print("Progress saved. Exiting...")
        exit()
    elif choice == "quit":
        print("Exiting without saving.")
        exit()

    # Save comparison to cache
    if choice in ["1", "2"]:
        comparison_cache[key] = choice
        comparison_count += 1

    # Sort based on Aidan's preference
    if choice == "1":
        less.append(movie)
    elif choice == "2":
        greater.append(movie)

try:
    with open("unsorted.txt", "r") as f:
        unsorted_movies = [line.strip() for line in f.readlines()]
    with open("unsorted.txt", "w") as f:
        f.write("")

except FileNotFoundError:
    print("unsorted.txt not found. Using a default movie list.")
    unsorted_movies = ["Inception", "Men In Tights", "Pulp Fiction", "Shawshank", "Dark Knight"]

sorted_movies = []

for movie in unsorted_movies:
    sort(movie, sorted_movies)

save()