import json

with open(r"C:\Users\Joseph Dania\Desktop\Ai_search_engine\doc\function_graph.json") as f:
    graph = json.load(f)

visited = set()
rec_stack = set()
order = []
cycles = []

def dfs(func, path):
    if func in rec_stack:
        cycles.append(path + [func])
        return

    if func in visited:
        return

    visited.add(func)
    rec_stack.add(func)

    for dep in graph.get(func, []):
        # Only traverse functions defined in the graph
        if dep in graph:
            dfs(dep, path + [func])

    rec_stack.remove(func)
    order.append(func)  # post-order

# 🔑 THIS IS THE FIX
# Run DFS from every node
for func in graph:
    if func not in visited:
        dfs(func, [])

print("Dependency order:")
print(order)

print("\nCycles found:")
for c in cycles:
    print(" -> ".join(c))
