class UnionFind:
    """A Disjoint Set Union (DSU) structure optimized using union by rank.
    """
    def __init__(self, n):
        # Initialize parent array where each element is its own parent
        self.parent = list(range(n))
        # Initialize rank array for union optimization
        self.rank = [0] * n

    def find(self, i):
        """Finds the root of the set containing element i.
        
        FIX: Implemented path compression.
        """
        if self.parent[i] == i:
            return i
        
        # Path compression
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Unites the sets containing elements i and j, using union by rank."""
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Attach smaller rank tree under root of higher rank tree
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                # If ranks are the same, make one root the parent and increment its rank
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False


def find_mst(V, edges):
    """ 
    Calculates the Minimum Spanning Tree (MST) using Kruskal's algorithm.

    Args:
        V (int): The number of vertices.
        edges (list): List of edges (u, v, weight).

    Returns:
        tuple: (minimum_spanning_tree (list), total_weight (int))
    """
    uf = UnionFind(V)

    # Sort edges by weight in non-decreasing order
    sorted_edges = sorted(edges, key=lambda x: x[2])

    minimum_spanning_tree = []
    mst_weight = 0

    for u, v, weight in sorted_edges:
        root_u = uf.find(u)
        root_v = uf.find(v)

        # If the roots are different, adding this edge does not create a cycle
        if root_u != root_v:
            minimum_spanning_tree.append((u, v, weight))
            mst_weight += weight

            # Merge the sets
            uf.union(u, v)

        # Stop if we have V - 1 edges
        if len(minimum_spanning_tree) == V - 1:
            break

    return minimum_spanning_tree, mst_weight
