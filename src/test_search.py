from semantic_search import search_ai

results = search_ai("hello")
for r in results:
    print(r["name"], r["score"])
