import os
import sys
import requests
import folium
import webbrowser
import osmium  # Fast OSM parsing
import platform

if __name__ == "__main__":
    # Define base directory and OSM file path
    basedir = os.path.dirname(__file__)

    if platform.system() == "Windows":
        PATH_TO_OSM_FILES = os.path.join("..", "..", "assets", "osm_files")
    else:
        PATH_TO_OSM_FILES = os.path.join("..", "assets", "osm_files")

    os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)  # Ensure the directory exists

    # Bounding box setup (approx. 500m in degrees)
    latitude, longitude = 45.5394, -73.6250
    # delta = 0.00225  # ~500m in degrees
    delta = 0.0450
    min_lat, max_lat = latitude - delta, latitude + delta
    min_lon, max_lon = longitude - delta, longitude + delta

    # File paths
    osm_file = os.path.join(PATH_TO_OSM_FILES, "map.osm")
    road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
    path_file = os.path.join(PATH_TO_OSM_FILES, "path.txt")

    # Ensure the files exist
    for file in [road_network_file, path_file]:
        if not os.path.exists(file):
            os.open(file, os.O_CREAT)  # Create an empty file

    # Download OSM data if not already downloaded
    if not os.path.exists(osm_file):
        osm_url = f"https://overpass-api.de/api/map?bbox={min_lon},{min_lat},{max_lon},{max_lat}"
        response = requests.get(osm_url)
        with open(osm_file, 'wb') as file:
            file.write(response.content)
        print(f"OSM data saved as '{osm_file}'")

    # Step 1: Extract node locations
    class NodeLocationHandler(osmium.SimpleHandler):
        def __init__(self):
            super().__init__()
            self.node_locations = {}  # Store node_id -> (lat, lon)

        def node(self, n):
            if n.location.valid():
                self.node_locations[n.id] = (n.location.lat, n.location.lon)

    # Step 2: Extract road network (nodes & unique bidirectional edges)
    class RoadNetworkHandler(osmium.SimpleHandler):
        def __init__(self, node_locations):
            super().__init__()
            self.node_locations = node_locations
            self.road_nodes = {}  # node_id -> (lat, lon)
            self.road_edges = set()  # Unique edges stored as (min_id, max_id) to avoid duplicates
        
        def way(self, w):
            if 'highway' in w.tags:  # Process only road networks
                prev_node_id = None
                for node in w.nodes:
                    if node.ref in self.node_locations:
                        self.road_nodes[node.ref] = self.node_locations[node.ref]

                        if prev_node_id is not None:
                            edge = tuple(sorted([prev_node_id, node.ref]))  # Store edges uniquely
                            self.road_edges.add(edge)

                        prev_node_id = node.ref  # Update previous node

    # Step 1: Get all node locations
    node_handler = NodeLocationHandler()
    node_handler.apply_file(osm_file)

    # Step 2: Process roads (nodes & unique edges)
    road_handler = RoadNetworkHandler(node_handler.node_locations)
    road_handler.apply_file(osm_file)

    # Save road network (Nodes & Edges) in new format
    with open(road_network_file, "w") as file:
        file.write("Nodes:\n")
        for node_id, (lat, lon) in road_handler.road_nodes.items():
            file.write(f"{node_id}: {lat}, {lon}\n")
        
        file.write("\nEdges:\n")
        for source, target in sorted(road_handler.road_edges):
            file.write(f"{source} <-> {target}\n")

    print(f"Filtered road network saved to {road_network_file}")