from semantic_search import search_ai

results = search_ai("how to log in a user")
for r in results:
    print(r["name"], r["score"])
