import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx

class Node:
    def __init__(self, node_id, position):
        self.node_id = node_id
        self.position = position  # (x, y)
        self.power = 2  # Slightly increased initial transmission power
        self.neighbors = []  # List of neighboring nodes

    def distance_to(self, other):
        return np.linalg.norm(np.array(self.position) - np.array(other.position))


def broadcast_hello(node, power, nodes):
    """Broadcast 'Hello' message and collect Acks."""
    for other in nodes:
        if other.node_id != node.node_id and node.distance_to(other) <= power:
            if other not in node.neighbors:
                node.neighbors.append(other)


def check_cone_coverage(node, angle):
    """Check if each cone of degree 'angle' around the node has at least one neighbor."""
    if not node.neighbors:
        return False

    angles = sorted([
        np.arctan2(n.position[1] - node.position[1], n.position[0] - node.position[0]) 
        for n in node.neighbors
    ])
    
    angles += [a + 2 * np.pi for a in angles]  # Ensure circular coverage
    for i in range(len(angles) - 1):
        if angles[i + 1] - angles[i] > angle:
            return False
    return True


def run_cbtc(nodes, angle, initial_power, max_power, shrink_back=False, asymmetric_removal=False):
    """Run the CBTC algorithm with optional optimizations."""
    for node in nodes:
        power = initial_power
        while power <= max_power:
            broadcast_hello(node, power, nodes)
            if check_cone_coverage(node, angle):
                node.power = power  # Store final power
                break
            power *= 1.5  # Adaptive power increase

        if shrink_back:
            apply_shrink_back(node, angle)
        
        if asymmetric_removal:
            remove_asymmetric_edges(node, nodes)


def apply_shrink_back(node, angle):
    """Reduce transmission power while maintaining cone coverage and connectivity."""
    sorted_neighbors = sorted(node.neighbors, key=lambda n: node.distance_to(n), reverse=True)
    for neighbor in sorted_neighbors:
        if len(node.neighbors) <= 3:  # Ensure at least 3 neighbors remain
            break
        node.neighbors.remove(neighbor)
        if not check_cone_coverage(node, angle):  # Ensure connectivity remains
            node.neighbors.append(neighbor)
            break


def remove_asymmetric_edges(node, nodes):
    """Remove asymmetric edges where one node sees the other but not vice versa."""
    node.neighbors = [n for n in node.neighbors if node in n.neighbors]
    
    # Ensure the node keeps at least one neighbor if possible
    if len(node.neighbors) == 0 and len(nodes) > 1:
        closest_node = min(nodes, key=lambda n: node.distance_to(n) if n != node else float('inf'))
        node.neighbors.append(closest_node)  # Add the closest available node


def visualize_network(nodes, title, ax):
    """Visualize the network topology."""
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.node_id, pos=node.position)
        for neighbor in node.neighbors:
            G.add_edge(node.node_id, neighbor.node_id)

    pos = nx.get_node_attributes(G, 'pos')
    ax.set_title(title)
    nx.draw(G, pos, ax=ax, with_labels=False, node_size=50, edge_color='black')


def generate_networks():
    """Generate and visualize different CBTC optimization scenarios."""
    num_nodes = 100
    area_size = 100
    angle = 2*np.pi / 3  # 120 degrees (from the paper)
    max_power = 20
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    scenarios = [
        {"title": "(a) No topology control", "shrink_back": False, "asymmetric_removal": False},
        {"title": "(b) α = 2π/3, CBTC", "shrink_back": False, "asymmetric_removal": False},
        {"title": "(c) α = 5π/6, CBTC", "shrink_back": False, "asymmetric_removal": False},
        {"title": "(d) α = 2π/3 with shrink-back", "shrink_back": True, "asymmetric_removal": False},
        {"title": "(e) α = 5π/6 with shrink-back", "shrink_back": True, "asymmetric_removal": False},
        {"title": "(f) α = 2π/3 with shrink-back and asymmetric edge removal", "shrink_back": True, "asymmetric_removal": True},
        {"title": "(g) α = 5π/6 with all optimizations", "shrink_back": True, "asymmetric_removal": True},
        {"title": "(h) α = 2π/3 with all optimizations", "shrink_back": True, "asymmetric_removal": True},
    ]

    for i, scenario in enumerate(scenarios):
        # Ensure full connectivity for No Topology Control
        if "No topology control" in scenario["title"]:
            initial_power = max_power  # Use maximum power for full connectivity
        else:
            initial_power = 2  # Controlled power for other cases

        nodes = [Node(i, (random.uniform(0, area_size), random.uniform(0, area_size))) for i in range(num_nodes)]
        run_cbtc(nodes, angle if '5π/6' not in scenario['title'] else 5*np.pi/6, initial_power, max_power, 
                 scenario['shrink_back'], scenario['asymmetric_removal'])
        visualize_network(nodes, scenario['title'], axes[i//4, i%4])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generate_networks()