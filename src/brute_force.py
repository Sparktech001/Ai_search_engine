import pandas as pd
import timeit
dataset = pd.read_csv("C:/Users/Joseph Dania/Desktop/Ai_search_engine/function_calls.csv")
data = dataset["functions calls cleaned"].dropna()
words = []
for info in data:
    parts = info.split(",")
    for part in parts:
        part = part.strip().lower()
        words.append(part)
def brute_force(word):
    result = []
    for data in words:
        if data.startswith(word):
            result.append(data)
    return result

users_search = input("Enter the word to search: ").strip().lower()

time_taken = timeit.timeit(
    stmt='brute_force(users_search)',
    number=1000,
    globals=globals()
)

print("Search results:", brute_force(users_search))
print(f"Brute-force search time (1000 runs): {time_taken} seconds")