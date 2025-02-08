import json

# Load movies from a file or use a default list
try:
    with open("test_text.txt", "r") as f:
        movies = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print("movies.txt not found. Using a default movie list.")
    movies = ["Inception", "Men In Tights", "Pulp Fiction", "Shawshank", "Dark Knight"]


def quicksort_movies(movies, comparison_cache, comparison_count):
    if len(movies) <= 1:
        return movies, comparison_count

    # Choose the pivot
    pivot = movies[len(movies) // 2]
    less = []
    greater = []

    for movie in movies:
        if movie == pivot:
            continue

        # Check cache for existing comparison
        key = tuple(sorted([movie, pivot]))
        if key in comparison_cache:
            choice = comparison_cache[key]
        else:
            # Ask Aidan for input
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

    # Recursively sort sublists
    save_progress(movies, comparison_cache, "progress.json")
    sorted_less, comparison_count = quicksort_movies(less, comparison_cache, comparison_count)
    sorted_greater, comparison_count = quicksort_movies(greater, comparison_cache, comparison_count)

    return sorted_less + [pivot] + sorted_greater, comparison_count

def save_progress(movies, comparison_cache, filename):
    try:
        # Convert tuple keys in comparison_cache to strings
        stringified_cache = {str(key): value for key, value in comparison_cache.items()}
        
        with open(filename, "w") as f:
            json.dump({"movies": movies, "cache": stringified_cache}, f, indent=4)
        print(f"Progress saved to {filename}.")
    except Exception as e:
        print(f"An error occurred while saving progress: {e}")


def load_progress(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"Loaded progress from {filename}.")
        return data.get("movies", []), data.get("cache", {})
    except FileNotFoundError:
        return None, {}  

def main():
    # Load saved progress
    loaded_movies, comparison_cache = load_progress("progress.json")
    if loaded_movies:  # If saved progress exists, use it
        movies = loaded_movies
    comparison_count = 0

    # Start ranking
    print("Starting movie ranking...")
    ranked_movies, comparison_count = quicksort_movies(movies, comparison_cache, comparison_count)

    # Show results
    print("\nFinal Ranked List:")
    for i, movie in enumerate(ranked_movies, 1):
        print(f"{i}. {movie}")

    print(f"\nTotal comparisons made: {comparison_count}")

    # Save results to a file
    with open("ranked_movies.txt", "w") as f:
        for movie in ranked_movies:
            f.write(f"{movie}\n")
    print("Ranked list saved to ranked_movies.txt.")

if __name__ == "__main__":
    main()
