import heapq

def find_shortest_paths(graph, start_node):
    """ 
    Implements Dijkstra's algorithm using a priority queue to find the shortest distance
    from a starting node to all other reachable nodes in a weighted graph 
    with non-negative edges.
    
    Args:
        graph (dict): Adjacency dictionary mapping nodes to a list of (neighbor, weight) tuples.
        start_node: The starting node.
        
    Returns:
        tuple: (distances, predecessors) dictionaries.
    """
    
    # Collect all nodes for initialization robustness
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        for neighbor, _ in neighbors:
            all_nodes.add(neighbor)
            
    distances = {node: float('inf') for node in all_nodes}
    
    if start_node not in distances:
        distances[start_node] = float('inf')
        
    distances[start_node] = 0
    
    # Initialize priority queue and push start node
    priority_queue = [(0, start_node)]
    
    # Initialize predecessors
    predecessors = {}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Check for stale entry
        if current_distance > distances[current_node]:
            continue
        
        if current_node not in graph:
            continue
            
        # Iterate through neighbors and relax edges
        for neighbor, weight in graph[current_node]:
            new_distance = current_distance + weight
            
            # FIX: Must use strict inequality (<) for relaxation. Using <= causes unnecessary heap insertions.
            if new_distance < distances.get(neighbor, float('inf')):
                
                # Ensure neighbor is tracked in distances if found for the first time
                if neighbor not in distances:
                    distances[neighbor] = float('inf')

                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))
                
    return distances, predecessors