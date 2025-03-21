# import os
# import folium
# import platform

# # Define base directory and OSM file path
# basedir = os.path.dirname(__file__)
# if platform.system() == "Windows":
#     PATH_TO_OSM_FILES = os.path.join("..", "..", "assets", "osm_files")
# else:
#     PATH_TO_OSM_FILES = os.path.join("..", "assets", "osm_files")
# road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")

# # Read node and edge data from the text file
# nodes = {}
# edges = []

# with open(road_network_file, "r") as file:
#     lines = file.readlines()

# # Parse Nodes
# node_section = False
# edge_section = False

# for line in lines:
#     line = line.strip()
    
#     if line == "Nodes:":
#         node_section = True
#         edge_section = False
#         continue
#     elif line == "Edges:":
#         node_section = False
#         edge_section = True
#         continue

#     # Process nodes
#     if node_section and line:
#         try:
#             node_id, coords = line.split(":")
#             lat, lon = map(float, coords.strip().split(","))
#             nodes[int(node_id)] = (lat, lon)
#         except ValueError:
#             continue  # Ignore malformed lines

#     # Process edges
#     if edge_section and line:
#         try:
#             source, target = line.split("<->")
#             edges.append((int(source.strip()), int(target.strip())))
#         except ValueError:
#             continue  # Ignore malformed lines

# # Create a Folium map
# latitude, longitude = 45.5394, -73.6250  # Center coordinates
# m = folium.Map(location=[latitude, longitude], zoom_start=16)

# # Plot nodes
# for node_id, (lat, lon) in nodes.items():
#     folium.CircleMarker(
#         location=[lat, lon],
#         radius=2,
#         color="red",
#         fill=True,
#         fill_color="red",
#         fill_opacity=0.7
#     ).add_to(m)

# # Plot edges
# for source, target in edges:
#     if source in nodes and target in nodes:
#         lat1, lon1 = nodes[source]
#         lat2, lon2 = nodes[target]
#         folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue", weight=2).add_to(m)

# # Save and open the map
# map_file = os.path.join(PATH_TO_OSM_FILES, "graph_map.html")
# m.save(map_file)
# print(f"Graph map saved as {map_file}")



import os
import folium
import platform
import webbrowser

# Define base directory and OSM file path
basedir = os.path.dirname(__file__)
if platform.system() == "Windows":
    PATH_TO_OSM_FILES = os.path.join("..", "..", "assets", "osm_files")
else:
    PATH_TO_OSM_FILES = os.path.join("..", "assets", "osm_files")

road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
path_file = os.path.join(PATH_TO_OSM_FILES, "path.txt")

# Read the path file
with open(path_file, "r") as file:
    path_nodes = {int(line.strip()) for line in file if line.strip().isdigit()}

# Read node and edge data from the text file
nodes = {}
edges = []

with open(road_network_file, "r") as file:
    lines = file.readlines()

# Parse Nodes
node_section = False
edge_section = False

for line in lines:
    line = line.strip()
    
    if line == "Nodes:":
        node_section = True
        edge_section = False
        continue
    elif line == "Edges:":
        node_section = False
        edge_section = True
        continue

    # Process nodes
    if node_section and line:
        try:
            node_id, coords = line.split(":")
            lat, lon = map(float, coords.strip().split(","))
            node_id = int(node_id)
            if node_id in path_nodes:  # Store only nodes in path.txt
                nodes[node_id] = (lat, lon)
        except ValueError:
            continue  # Ignore malformed lines

    # Process edges
    if edge_section and line:
        try:
            source, target = line.split("<->")
            source, target = int(source.strip()), int(target.strip())
            if source in nodes and target in nodes:
                edges.append((source, target))
        except ValueError:
            continue  # Ignore malformed lines

# Create a Folium map centered at the first node in the path
if nodes:
    first_node = next(iter(nodes.values()))
    m = folium.Map(location=[first_node[0], first_node[1]], zoom_start=16)

    # Plot nodes in the path
    for node_id, (lat, lon) in nodes.items():
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            popup=str(node_id)
        ).add_to(m)

    # Plot edges in the path
    for source, target in edges:
        lat1, lon1 = nodes[source]
        lat2, lon2 = nodes[target]
        folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue", weight=2).add_to(m)

    # Save and open the map
    map_file = os.path.join(PATH_TO_OSM_FILES, "graph_path.html")
    m.save(map_file)
    print(f"Path map saved as {map_file}")

    webbrowser.open(map_file)

else:
    print("No nodes found in path.txt that match the road network file.")


