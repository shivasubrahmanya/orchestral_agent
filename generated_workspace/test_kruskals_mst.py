import pytest
from kruskals_mst import find_mst


def test_kruskal_standard_connected_graph():
    # V=4, Standard connected graph example
    V = 4
    edges = [
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4)
    ]
    # MST edges: (2, 3, 4), (0, 3, 5), (0, 1, 10). Total weight = 19.
    expected_weight = 19
    expected_num_edges = 3
    
    mst_edges, total_weight = find_mst(V, edges)
    
    assert total_weight == expected_weight
    assert len(mst_edges) == expected_num_edges


def test_kruskal_larger_graph_with_many_cycles():
    # V=9, A denser graph ensuring cycle detection works correctly
    V = 9
    edges = [
        (0, 1, 4), (0, 7, 8),
        (1, 2, 8), (1, 7, 11),
        (2, 3, 7), (2, 8, 2), (2, 5, 4),
        (3, 4, 9), (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1), (6, 8, 6),
        (7, 8, 7)
    ]
    # Expected MST weight: 1 + 2 + 2 + 4 + 4 + 7 + 8 + 9 = 37
    expected_weight = 37
    expected_num_edges = 8  # V - 1
    
    mst_edges, total_weight = find_mst(V, edges)
    
    assert total_weight == expected_weight
    assert len(mst_edges) == expected_num_edges


def test_kruskal_disconnected_graph():
    # V=5, two components (0, 1, 2) and isolated (3, 4).
    V = 5
    edges = [
        (0, 1, 5),
        (1, 2, 3),
        (0, 2, 1)
    ]
    # MST: (0, 2, 1) + (1, 2, 3) = 4. Only 2 edges needed for component size 3.
    expected_weight = 4
    expected_num_edges = 2 
    
    mst_edges, total_weight = find_mst(V, edges)
    
    assert total_weight == expected_weight
    assert len(mst_edges) == expected_num_edges


def test_kruskal_single_vertex_graph():
    # V=1, E=0.
    V = 1
    edges = []
    expected_weight = 0
    expected_num_edges = 0
    
    mst_edges, total_weight = find_mst(V, edges)
    
    assert total_weight == expected_weight
    assert len(mst_edges) == expected_num_edges


def test_kruskal_zero_weight_edges():
    # Ensure zero weight edges are handled correctly and prioritize
    V = 3
    edges = [
        (0, 1, 0),
        (1, 2, 5),
        (0, 2, 10)
    ]
    # MST: (0, 1, 0) + (1, 2, 5). Total weight 5.
    expected_weight = 5
    expected_num_edges = 2

    mst_edges, total_weight = find_mst(V, edges)

    assert total_weight == expected_weight
    assert len(mst_edges) == expected_num_edges
