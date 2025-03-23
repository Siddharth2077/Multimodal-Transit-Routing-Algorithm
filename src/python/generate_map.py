# # import os
# # import requests
# # import osmium  # Fast OSM parsing
# # import sys
# # import platform

# # if __name__ == "__main__":
# #     # Define base directory and OSM file path
# #     if platform.system() == "Windows":
# #         PATH_TO_OSM_FILES = os.path.join("..", "..", "assets", "osm_files")
# #     else:
# #         PATH_TO_OSM_FILES = os.path.join("..", "assets", "osm_files")
# #     os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)  # Ensure the directory exists

# #     # Bounding box setup (approx. 5x5 km in degrees)
# #     latitude, longitude = 45.5394, -73.6250
# #     delta = 0.045  # 5x5 km in degrees
# #     min_lat, max_lat = latitude - delta, latitude + delta
# #     min_lon, max_lon = longitude - delta, longitude + delta

# #     # File paths
# #     osm_file = os.path.join(PATH_TO_OSM_FILES, "map.osm")
# #     road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
# #     path_file = os.path.join(PATH_TO_OSM_FILES, "path.txt")

# #     # Ensure the files exist
# #     for file in [road_network_file, path_file]:
# #         if not os.path.exists(file):
# #             os.open(file, os.O_CREAT)  # Create an empty file

# #     # Download OSM data if not already downloaded
# #     if not os.path.exists(osm_file):
# #         osm_url = f"https://overpass-api.de/api/map?bbox={min_lon},{min_lat},{max_lon},{max_lat}"
# #         response = requests.get(osm_url)
# #         with open(osm_file, 'wb') as file:
# #             file.write(response.content)
# #         print(f"OSM data saved as '{osm_file}'")

# #     # Step 1: Extract all node locations
# #     class NodeLocationHandler(osmium.SimpleHandler):
# #         def __init__(self):
# #             super().__init__()
# #             self.node_locations = {}  # Store node_id -> (lat, lon)

# #         def node(self, n):
# #             if n.location.valid():
# #                 self.node_locations[n.id] = (n.location.lat, n.location.lon)

# #     node_handler = NodeLocationHandler()
# #     node_handler.apply_file(osm_file)

# #     # Step 2: Extract road network (using only road nodes)
# #     class RoadNetworkHandler(osmium.SimpleHandler):
# #         def __init__(self, node_locations):
# #             super().__init__()
# #             self.node_locations = node_locations
# #             self.road_nodes = {}  # node_id -> (lat, lon)
# #             self.road_edges = set()  # Unique edges stored as (min_id, max_id)

# #         def way(self, w):
# #             if 'highway' in w.tags:  # Process only road networks
# #                 way_nodes = []
# #                 for node in w.nodes:
# #                     if node.ref in self.node_locations:  # Only add valid nodes
# #                         self.road_nodes[node.ref] = self.node_locations[node.ref]
# #                         way_nodes.append(node.ref)

# #                 # Create edges for consecutive nodes
# #                 for i in range(len(way_nodes) - 1):
# #                     edge = tuple(sorted([way_nodes[i], way_nodes[i + 1]]))
# #                     self.road_edges.add(edge)

# #     # Process roads using previously extracted nodes
# #     road_handler = RoadNetworkHandler(node_handler.node_locations)
# #     road_handler.apply_file(osm_file)

# #     # Ensure road network is not empty
# #     if not road_handler.road_nodes or not road_handler.road_edges:
# #         print("Error: No road network data extracted.")
# #         sys.exit(1)

# #     # Save filtered road network (Nodes & Edges)
# #     with open(road_network_file, "w") as file:
# #         file.write("Nodes:\n")
# #         for node_id, (lat, lon) in road_handler.road_nodes.items():
# #             file.write(f"{node_id}: {lat}, {lon}\n")

# #         file.write("\nEdges:\n")
# #         for source, target in sorted(road_handler.road_edges):
# #             file.write(f"{source} <-> {target}\n")

# #     print(f"Filtered road network saved to {road_network_file}")

# import os
# import requests
# import osmium  # Fast OSM parsing
# import sys
# import platform
# import math

# if __name__ == "__main__":
#     # Define base directory and OSM file path
#     # if platform.system() == "Windows":
#     #     PATH_ADAPTER = ".."
#     # else:
#     #     PATH_ADAPTER = ""
#     PATH_ADAPTER = ".."
#     PATH_TO_OSM_FILES = os.path.join(PATH_ADAPTER, "..", "assets", "osm_files")
#     PATH_TO_BUS_STOPS = os.path.join(PATH_ADAPTER, "..", "assets", "bus_stops")
#     os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)
#     os.makedirs(PATH_TO_BUS_STOPS, exist_ok=True)  

#     # Bounding box setup (approx. 5x5 km in degrees)
#     latitude, longitude = 45.5394, -73.6250
#     delta = 0.045  # 5x5 km in degrees
#     min_lat, max_lat = latitude - delta, latitude + delta
#     min_lon, max_lon = longitude - delta, longitude + delta

#     # File paths
#     osm_file = os.path.join(PATH_TO_OSM_FILES, "map.osm")
#     road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
#     path_file = os.path.join(PATH_TO_OSM_FILES, "path.txt")
#     stop_nodes_file = os.path.join(PATH_TO_BUS_STOPS, "stop_nodes.txt")
#     stops_txt_file = os.path.join(PATH_TO_BUS_STOPS, "stops.txt")

#     # Ensure the files exist
#     for file in [road_network_file, path_file, stop_nodes_file]:
#         if not os.path.exists(file):
#             os.open(file, os.O_CREAT)  # Create an empty file

#     # Download OSM data if not already downloaded
#     if not os.path.exists(osm_file):
#         osm_url = f"https://overpass-api.de/api/map?bbox={min_lon},{min_lat},{max_lon},{max_lat}"
#         response = requests.get(osm_url)
#         with open(osm_file, 'wb') as file:
#             file.write(response.content)
#         print(f"OSM data saved as '{osm_file}'")

#     # Step 1: Extract all node locations
#     class NodeLocationHandler(osmium.SimpleHandler):
#         def __init__(self):
#             super().__init__()
#             self.node_locations = {}  # Store node_id -> (lat, lon)

#         def node(self, n):
#             if n.location.valid():
#                 self.node_locations[n.id] = (n.location.lat, n.location.lon)

#     node_handler = NodeLocationHandler()
#     node_handler.apply_file(osm_file)

#     # Step 2: Extract road network (using only road nodes)
#     class RoadNetworkHandler(osmium.SimpleHandler):
#         def __init__(self, node_locations):
#             super().__init__()
#             self.node_locations = node_locations
#             self.road_nodes = {}  # node_id -> (lat, lon)
#             self.road_edges = set()  # Unique edges stored as (min_id, max_id)

#         def way(self, w):
#             if 'highway' in w.tags:  # Process only road networks
#                 way_nodes = []
#                 for node in w.nodes:
#                     if node.ref in self.node_locations:  # Only add valid nodes
#                         self.road_nodes[node.ref] = self.node_locations[node.ref]
#                         way_nodes.append(node.ref)

#                 # Create edges for consecutive nodes
#                 for i in range(len(way_nodes) - 1):
#                     edge = tuple(sorted([way_nodes[i], way_nodes[i + 1]]))
#                     self.road_edges.add(edge)

#     # Process roads using previously extracted nodes
#     road_handler = RoadNetworkHandler(node_handler.node_locations)
#     road_handler.apply_file(osm_file)

#     # Ensure road network is not empty
#     if not road_handler.road_nodes or not road_handler.road_edges:
#         print("Error: No road network data extracted.")
#         sys.exit(1)

#     # Save filtered road network (Nodes & Edges)
#     with open(road_network_file, "w") as file:
#         file.write("Nodes:\n")
#         for node_id, (lat, lon) in road_handler.road_nodes.items():
#             file.write(f"{node_id}: {lat}, {lon}\n")

#         file.write("\nEdges:\n")
#         for source, target in sorted(road_handler.road_edges):
#             file.write(f"{source} <-> {target}\n")

#     print(f"Filtered road network saved to {road_network_file}")

#     # Step 3: Load bus stops and filter them based on bounding box
#     def is_within_bounds(lat, lon):
#         return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon

#     bus_stops = []
#     with open(stops_txt_file, "r") as file:
#         next(file)  # Skip header
#         for line in file:
#             parts = line.strip().split(",")
#             if len(parts) < 5:
#                 continue
#             stop_id, stop_name, stop_lat, stop_lon = parts[0], parts[2], float(parts[3]), float(parts[4])
#             if is_within_bounds(stop_lat, stop_lon):
#                 bus_stops.append((stop_id, stop_name, stop_lat, stop_lon))

#     # Step 4: Find nearest road network node for each bus stop
#     def haversine(lat1, lon1, lat2, lon2):
#         R = 6371  # Earth radius in km
#         dlat = math.radians(lat2 - lat1)
#         dlon = math.radians(lon2 - lon1)
#         a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
#         return 2 * R * math.asin(math.sqrt(a))

#     bus_stop_nodes = {}
#     for stop_id, stop_name, stop_lat, stop_lon in bus_stops:
#         nearest_node = min(road_handler.road_nodes.items(), key=lambda item: haversine(stop_lat, stop_lon, item[1][0], item[1][1]))
#         bus_stop_nodes[stop_id] = (nearest_node[0], stop_name, nearest_node[1][0], nearest_node[1][1])

#     # Step 5: Save bus stop nodes
#     with open(stop_nodes_file, "w") as file:
#         file.write("Bus Stop Nodes:\n")
#         for stop_id, (node_id, stop_name, lat, lon) in bus_stop_nodes.items():
#             file.write(f"{stop_id} ({stop_name}) -> {node_id}: {lat}, {lon}\n")

#     print(f"Filtered bus stop nodes saved to {stop_nodes_file}")

import os
import requests
import osmium  # Fast OSM parsing
import sys
import platform
import math
import csv

if __name__ == "__main__":
    PATH_ADAPTER = ".."
    PATH_TO_OSM_FILES = os.path.join(PATH_ADAPTER, "..", "assets", "osm_files")
    PATH_TO_BUS_STOPS = os.path.join(PATH_ADAPTER, "..", "assets", "bus_stops")
    os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)
    os.makedirs(PATH_TO_BUS_STOPS, exist_ok=True)  

    latitude, longitude = 45.5394, -73.6250
    delta = 0.045
    min_lat, max_lat = latitude - delta, latitude + delta
    min_lon, max_lon = longitude - delta, longitude + delta

    osm_file = os.path.join(PATH_TO_OSM_FILES, "map.osm")
    road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
    stop_nodes_file = os.path.join(PATH_TO_BUS_STOPS, "stop_nodes.txt")
    trips_file = os.path.join(PATH_TO_BUS_STOPS, "trips.txt")
    stops_txt_file = os.path.join(PATH_TO_BUS_STOPS, "stops.txt")
    stop_times_txt_file = os.path.join(PATH_TO_BUS_STOPS, "stop_times.txt")

    class NodeLocationHandler(osmium.SimpleHandler):
        def __init__(self):
            super().__init__()
            self.node_locations = {}

        def node(self, n):
            if n.location.valid():
                self.node_locations[n.id] = (n.location.lat, n.location.lon)

    node_handler = NodeLocationHandler()
    node_handler.apply_file(osm_file)

    class RoadNetworkHandler(osmium.SimpleHandler):
        def __init__(self, node_locations):
            super().__init__()
            self.node_locations = node_locations
            self.road_nodes = {}

        def way(self, w):
            if 'highway' in w.tags:
                for node in w.nodes:
                    if node.ref in self.node_locations:
                        self.road_nodes[node.ref] = self.node_locations[node.ref]

    road_handler = RoadNetworkHandler(node_handler.node_locations)
    road_handler.apply_file(osm_file)

    def is_within_bounds(lat, lon):
        return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon

    bus_stops = {}
    with open(stops_txt_file, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            stop_id, stop_name, stop_lat, stop_lon = row[0], row[2], float(row[3]), float(row[4])
            if is_within_bounds(stop_lat, stop_lon):
                bus_stops[stop_id] = (stop_name, stop_lat, stop_lon)

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return 2 * R * math.asin(math.sqrt(a))

    bus_stop_nodes = {}
    for stop_id, (stop_name, stop_lat, stop_lon) in bus_stops.items():
        nearest_node = min(road_handler.road_nodes.items(), key=lambda item: haversine(stop_lat, stop_lon, item[1][0], item[1][1]))
        bus_stop_nodes[stop_id] = (nearest_node[0], stop_name, nearest_node[1][0], nearest_node[1][1])

    with open(stop_nodes_file, "w") as file:
        file.write("Bus Stop Nodes:\n")
        for stop_id, (node_id, stop_name, lat, lon) in bus_stop_nodes.items():
            file.write(f"{stop_id} ({stop_name}) -> {node_id}: {lat}, {lon}\n")

    trips = {}
    with open(stop_times_txt_file, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            trip_id, stop_id, stop_sequence = row[0], row[3], int(row[4])
            if stop_id in bus_stop_nodes:
                node_id = bus_stop_nodes[stop_id][0]
                if trip_id not in trips:
                    trips[trip_id] = []
                trips[trip_id].append((stop_sequence, node_id))
    
    with open(trips_file, "w") as file:
        file.write("Trip Sequences:\n")
        for trip_id, nodes in trips.items():
            nodes.sort()  # Sort by stop_sequence
            node_list = [str(node[1]) for node in nodes]
            file.write(f"{trip_id}: {', '.join(node_list)}\n")

    print(f"Trip sequences saved to {trips_file}")