import pytest
from dijkstra_solver import find_shortest_paths
import math

# Test case 1: Standard graph with multiple paths and unreachable nodes
def test_dijkstra_basic_functionality():
    # Graph: A -> B (1), A -> C (4), B -> C (2), B -> D (5), C -> D (1), D -> E (3)
    # F and G are isolated.
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': [('E', 3)],
        'E': [],
        'F': [('G', 10)],
        'G': []
    }
    start_node = 'A'

    # Expected shortest distances from 'A'
    expected_distances = {
        'A': 0,
        'B': 1,
        'C': 3,  # Path A -> B -> C (1 + 2)
        'D': 4,  # Path A -> B -> C -> D (1 + 2 + 1)
        'E': 7,  # Path A -> B -> C -> D -> E (4 + 3)
        'F': float('inf'), # Unreachable
        'G': float('inf')  # Unreachable
    }

    # Expected predecessors for path reconstruction
    expected_predecessors = {
        'B': 'A',
        'C': 'B',
        'D': 'C',
        'E': 'D'
    }

    distances, predecessors = find_shortest_paths(graph, start_node)

    # 1. Verify distances
    assert set(distances.keys()) == set(expected_distances.keys())
    
    for node, dist in expected_distances.items():
        if math.isinf(dist):
            assert math.isinf(distances[node]), f"Distance to {node} should be infinity."
        else:
            assert distances[node] == dist, f"Incorrect distance for node {node}. Expected {dist}, got {distances[node]}"

    # 2. Verify predecessors
    
    # Filter actual predecessors to only include keys expected to have a defined path
    actual_predecessors_filtered = {k: v for k, v in predecessors.items() if k in expected_predecessors}
    
    assert actual_predecessors_filtered == expected_predecessors, "Incorrect predecessors dictionary for reachable nodes."

# Test case 2: Graph with zero weights
def test_dijkstra_zero_weights():
    graph = {
        'S': [('A', 0), ('B', 5)],
        'A': [('B', 1)],
        'B': [('T', 1)],
        'T': []
    }
    start_node = 'S'
    
    # Shortest path S->A->B->T (0 + 1 + 1 = 2)
    
    expected_distances = {
        'S': 0,
        'A': 0, 
        'B': 1, 
        'T': 2 
    }
    
    expected_predecessors = {
        'A': 'S',
        'B': 'A', 
        'T': 'B'
    }
    
    distances, predecessors = find_shortest_paths(graph, start_node)
    
    assert distances == expected_distances
    
    actual_predecessors_filtered = {k: v for k, v in predecessors.items() if k in expected_predecessors}
    assert actual_predecessors_filtered == expected_predecessors

# Test case 3: Single node graph
def test_dijkstra_single_node():
    graph = {'A': []}
    start_node = 'A'
    
    expected_distances = {'A': 0}
    expected_predecessors = {}
    
    distances, predecessors = find_shortest_paths(graph, start_node)
    
    assert distances == expected_distances
    
    # Ensure predecessors is empty or only contains non-critical info (like start node pointing to None)
    actual_predecessors_filtered = {k: v for k, v in predecessors.items() if k != start_node}
    assert actual_predecessors_filtered == expected_predecessors