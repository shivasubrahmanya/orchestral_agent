import heapq
import math

def dijkstra_shortest_path(graph, start_node):
    """ 
    Implements Dijkstra's algorithm to find the shortest path from a source node
    to all other nodes in a weighted graph with non-negative edge weights.
    
    Note: Contains a subtle logic bug in the stale entry check.
    """
    
    # 1. Initialization
    # Ensure we cover all nodes defined in the graph structure, including neighbors
    # that might not be keys themselves but appear in adjacency lists.
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        for neighbor, _ in neighbors:
            all_nodes.add(neighbor)

    distances = {node: math.inf for node in all_nodes}
    distances[start_node] = 0

    # 2. Priority Queue
    pq = [(0, start_node)] # (distance, node)

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        # --- FIXED LOGIC --- 
        # We must skip stale entries, where current_distance extracted from PQ 
        # is strictly greater than the currently recorded shortest distance.
        if current_distance > distances[current_node]:
            continue

        # 3. Relaxation
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                new_distance = current_distance + weight

                if new_distance < distances.get(neighbor, math.inf):
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))

    return distances

if __name__ == '__main__':
    # Example usage for testing the implementation/bug
    test_graph = {
        'A': [('B', 1), ('C', 10)],
        'B': [('C', 1)],
        'C': [('D', 1)]
    }
    
    # Expected output (Shortest paths):
    # A -> A: 0
    # A -> B: 1
    # A -> C: 2 (via B)
    # A -> D: 3 (via B, C)
    
    shortest_paths = dijkstra_shortest_path(test_graph, 'A')
    # print(shortest_paths)
