import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Function to compute SSD (Sum of Squared Differences)
def compute_ssd(list1, list2):
    rank_dict_1 = {movie: rank + 1 for rank, movie in enumerate(list1)}
    rank_dict_2 = {movie: rank + 1 for rank, movie in enumerate(list2)}
    return sum((rank_dict_1[movie] - rank_dict_2[movie]) ** 2 for movie in common_movies)

# Example rankings (same movies in different orders)
with open("aidan_sorted.txt", "r") as f:
        aidan_sorted_movies = [line.strip() for line in f.readlines()]
        ranked_list_1 = aidan_sorted_movies
with open("jonah_sorted.txt", "r") as f:
        jonah_sorted_movies = [line.strip() for line in f.readlines()]
        ranked_list_2 = jonah_sorted_movies

common_movies = list(set(ranked_list_1) & set(ranked_list_2))
ranked_list_1 = [movie for movie in ranked_list_1 if movie in common_movies]
ranked_list_2 = [movie for movie in ranked_list_2 if movie in common_movies]

# Compute SSD for actual input lists
actual_ssd = compute_ssd(ranked_list_1, ranked_list_2)

L = len(ranked_list_1)
s_max = (L*((L**2)-1))/3

print(f"Sum of Squared Differences: {actual_ssd}")
print(f"Maximum Sum of Squared Differences: {s_max}")
print("Sum/Max Sum: " + str(actual_ssd/s_max))

# Generate 1000 random ranking pairs and compute SSD
random_ssds = []
for _ in range(100000):
    random_list_1 = common_movies[:]  
    random_list_2 = common_movies[:]
    random.shuffle(random_list_1)
    random.shuffle(random_list_2)
    random_ssds.append(compute_ssd(random_list_1, random_list_2))

# Plot histogram of SSD values
plt.figure(figsize=(10, 6))
plt.hist(random_ssds, bins=30, color="skyblue", alpha=0.7, edgecolor="black", label="Random Pairs")
plt.axvline(actual_ssd, color="red", linestyle="dashed", linewidth=2, label="Actual SSD")
plt.xlabel("Sum of Squared Differences")
plt.ylabel("Frequency")
plt.title("Distribution of SSD for Random Rankings")
plt.legend()
plt.show()
