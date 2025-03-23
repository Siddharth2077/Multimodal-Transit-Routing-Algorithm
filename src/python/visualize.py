# # import os
# # import platform
# # import requests
# # import osmium
# # import pydeck as pdk
# # import sys

# # # Define paths
# # if platform.system() == "Windows":
# #     PATH_TO_OSM_FILES = os.path.join("..", "..", "assets", "osm_files")
# # else:
# #     PATH_TO_OSM_FILES = os.path.join("..", "assets", "osm_files")
# # os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)
# # road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
# # path_file = os.path.join(PATH_TO_OSM_FILES, "path.txt")
# # map_file = os.path.join(PATH_TO_OSM_FILES, "webgl_map.html")

# # # Check if required files exist
# # if not os.path.exists(road_network_file):
# #     print("Error: Road network file not found. Terminating program.")
# #     sys.exit(1)
# # if not os.path.exists(path_file):
# #     print("Error: Path file not found. Terminating program.")
# #     sys.exit(1)

# # # Parse road network file
# # nodes = {}
# # edges = []
# # with open(road_network_file, "r") as file:
# #     lines = file.readlines()
# #     parsing_nodes = False
# #     parsing_edges = False
    
# #     for line in lines:
# #         line = line.strip()
# #         if line == "Nodes:":
# #             parsing_nodes = True
# #             parsing_edges = False
# #             continue
# #         elif line == "Edges:":
# #             parsing_nodes = False
# #             parsing_edges = True
# #             continue
        
# #         if parsing_nodes and line:
# #             parts = line.split(": ")
# #             if len(parts) == 2:
# #                 node_id = parts[0]
# #                 lat, lon = map(float, parts[1].split(", "))
# #                 nodes[node_id] = [lon, lat]  # Pydeck uses [lon, lat]
        
# #         if parsing_edges and line:
# #             parts = line.split(" <-> ")
# #             if len(parts) == 2 and parts[0] in nodes and parts[1] in nodes:
# #                 edges.append({
# #                     "start": nodes[parts[0]],
# #                     "end": nodes[parts[1]]
# #                 })

# # # Parse path file
# # path_nodes = []
# # with open(path_file, "r") as file:
# #     for line in file:
# #         node_id = line.strip()
# #         if node_id in nodes:
# #             path_nodes.append(nodes[node_id])

# # # Generate Pydeck Map
# # road_layer = pdk.Layer(
# #     "LineLayer",
# #     edges,
# #     get_source_position="start",
# #     get_target_position="end",
# #     get_color=[43, 139, 196],  # Blue roads
# #     get_width=3,
# #     pickable=False # Disable hover effects
# # )

# # marker_layer = pdk.Layer(
# #     "ScatterplotLayer",
# #     [{"coordinates": coords, "node_id": node_id} for node_id, coords in nodes.items()],
# #     get_position="coordinates",
# #     get_color=[255, 0, 0, 255],  # Red nodes
# #     get_radius=.4,
# #     pickable=True,
# #     tooltip={"text": "{node_id}"}
# # )

# # path_layer = pdk.Layer(
# #     "LineLayer",
# #     [{"start": path_nodes[i], "end": path_nodes[i + 1]} for i in range(len(path_nodes) - 1)],
# #     get_source_position="start",
# #     get_target_position="end",
# #     get_color=[0, 255, 0],  # Green path
# #     get_width=4,
# #     pickable=False # Disable hover effects
# # )

# # # Center map on first node
# # if nodes:
# #     first_node = next(iter(nodes.values()))
# #     latitude, longitude = first_node[1], first_node[0]
# # else:
# #     print("Error: No nodes found in road network file. Terminating program.")
# #     sys.exit(1)

# # view_state = pdk.ViewState(
# #     latitude=latitude,
# #     longitude=longitude,
# #     zoom=16,
# #     pitch=30,
# #     bearing=0
# # )

# # deck = pdk.Deck(
# #     layers=[road_layer, marker_layer, path_layer],
# #     initial_view_state=view_state,
# #     map_style="mapbox://styles/mapbox/light-v9",
# #     tooltip={"html": "<b>Node ID:</b> {node_id}", "style": {"backgroundColor": "steelblue", "color": "white"}}
# # )

# # deck.to_html(map_file)
# # print(f"WebGL Map available at: http://localhost:8080/webgl_map.html")

# # # Start Local Server
# # os.system(f"cd {PATH_TO_OSM_FILES} && python -m http.server 8080")

# import os
# import platform
# import requests
# import osmium
# import pydeck as pdk
# import sys

# PATH_ADAPTER = ".."
# PATH_TO_OSM_FILES = os.path.join(PATH_ADAPTER, "..", "assets", "osm_files")
# PATH_TO_BUS_STOPS = os.path.join(PATH_ADAPTER, "..", "assets", "bus_stops")
# os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)
# os.makedirs(PATH_TO_BUS_STOPS, exist_ok=True)  

# road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
# path_file = os.path.join(PATH_TO_OSM_FILES, "path.txt")
# map_file = os.path.join(PATH_TO_OSM_FILES, "webgl_map.html")
# stop_nodes_file = os.path.join(PATH_TO_BUS_STOPS, "stop_nodes.txt")

# missing_files = [file for file in [road_network_file, path_file, stop_nodes_file] if not os.path.exists(file)]
# if missing_files:
#     print(f"Error: Missing files - {', '.join(missing_files)}. Terminating program.")
#     sys.exit(1)

# # Parse road network file
# nodes = {}
# edges = []
# with open(road_network_file, "r") as file:
#     lines = file.readlines()
#     parsing_nodes = False
#     parsing_edges = False
    
#     for line in lines:
#         line = line.strip()
#         if line == "Nodes:":
#             parsing_nodes = True
#             parsing_edges = False
#             continue
#         elif line == "Edges:":
#             parsing_nodes = False
#             parsing_edges = True
#             continue
        
#         if parsing_nodes and line:
#             parts = line.split(": ")
#             if len(parts) == 2:
#                 node_id = parts[0]
#                 lat, lon = map(float, parts[1].split(", "))
#                 nodes[node_id] = [lon, lat]  # Pydeck uses [lon, lat]
        
#         if parsing_edges and line:
#             parts = line.split(" <-> ")
#             if len(parts) == 2 and parts[0] in nodes and parts[1] in nodes:
#                 edges.append({
#                     "start": nodes[parts[0]],
#                     "end": nodes[parts[1]]
#                 })

# # Parse bus stop nodes file
# bus_nodes = {}
# with open(stop_nodes_file, "r") as file:
#     lines = file.readlines()
#     parsing_bus_nodes = False
    
#     for line in lines:
#         line = line.strip()
#         if line == "Bus Stop Nodes:":
#             parsing_bus_nodes = True
#             continue
        
#         if parsing_bus_nodes and "->" in line:
#             stop_id, node_info = line.split(" -> ")
#             node_id, coords = node_info.split(": ")
#             lat, lon = map(float, coords.split(", "))
#             bus_nodes[node_id] = [lon, lat]

# # Generate Pydeck Map
# road_layer = pdk.Layer(
#     "LineLayer",
#     edges,
#     get_source_position="start",
#     get_target_position="end",
#     get_color=[43, 139, 196],  # Blue roads
#     get_width=3,
#     pickable=False # Disable hover effects
# )

# bus_marker_layer = pdk.Layer(
#     "ScatterplotLayer",
#     [{"coordinates": coords, "node_id": node_id} for node_id, coords in bus_nodes.items()],
#     get_position="coordinates",
#     get_color=[255, 0, 0, 255],  # Red bus stop nodes
#     get_radius=4,
#     pickable=True,
#     tooltip={"text": "{node_id}"}
# )

# # Center map on first bus stop node
# if bus_nodes:
#     first_bus_node = next(iter(bus_nodes.values()))
#     latitude, longitude = first_bus_node[1], first_bus_node[0]
# else:
#     print("Error: No bus stop nodes found. Terminating program.")
#     sys.exit(1)

# view_state = pdk.ViewState(
#     latitude=latitude,
#     longitude=longitude,
#     zoom=16,
#     pitch=30,
#     bearing=0
# )

# deck = pdk.Deck(
#     layers=[road_layer, bus_marker_layer],
#     initial_view_state=view_state,
#     map_style="mapbox://styles/mapbox/light-v9",
#     tooltip={"html": "<b>Bus Stop Node ID:</b> {node_id}", "style": {"backgroundColor": "steelblue", "color": "white"}}
# )

# deck.to_html(map_file)
# print(f"WebGL Map available at: http://localhost:8080/webgl_map.html")

# # Start Local Server
# os.system(f"cd {PATH_TO_OSM_FILES} && python -m http.server 8080")

import os
import platform
import requests
import osmium
import pydeck as pdk
import sys

PATH_ADAPTER = ".."
PATH_TO_OSM_FILES = os.path.join(PATH_ADAPTER, "..", "assets", "osm_files")
PATH_TO_BUS_STOPS = os.path.join(PATH_ADAPTER, "..", "assets", "bus_stops")
os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)
os.makedirs(PATH_TO_BUS_STOPS, exist_ok=True)  

road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
path_file = os.path.join(PATH_TO_OSM_FILES, "path.txt")
map_file = os.path.join(PATH_TO_OSM_FILES, "webgl_map.html")
stop_nodes_file = os.path.join(PATH_TO_BUS_STOPS, "stop_nodes.txt")
trips_file = os.path.join(PATH_TO_BUS_STOPS, "trips.txt")

missing_files = [file for file in [road_network_file, path_file, stop_nodes_file, trips_file] if not os.path.exists(file)]
if missing_files:
    print(f"Error: Missing files - {', '.join(missing_files)}. Terminating program.")
    sys.exit(1)

# Parse road network file
nodes = {}
edges = []
with open(road_network_file, "r") as file:
    lines = file.readlines()
    parsing_nodes = False
    parsing_edges = False
    
    for line in lines:
        line = line.strip()
        if line == "Nodes:":
            parsing_nodes = True
            parsing_edges = False
            continue
        elif line == "Edges:":
            parsing_nodes = False
            parsing_edges = True
            continue
        
        if parsing_nodes and line:
            parts = line.split(": ")
            if len(parts) == 2:
                node_id = parts[0]
                lat, lon = map(float, parts[1].split(", "))
                nodes[node_id] = [lon, lat]  # Pydeck uses [lon, lat]
        
        if parsing_edges and line:
            parts = line.split(" <-> ")
            if len(parts) == 2 and parts[0] in nodes and parts[1] in nodes:
                edges.append({
                    "start": nodes[parts[0]],
                    "end": nodes[parts[1]]
                })

# Parse bus stop nodes file
bus_nodes = {}
with open(stop_nodes_file, "r") as file:
    lines = file.readlines()
    parsing_bus_nodes = False
    
    for line in lines:
        line = line.strip()
        if line == "Bus Stop Nodes:":
            parsing_bus_nodes = True
            continue
        
        if parsing_bus_nodes and "->" in line:
            stop_id, node_info = line.split(" -> ")
            node_id, coords = node_info.split(": ")
            lat, lon = map(float, coords.split(", "))
            bus_nodes[node_id] = [lon, lat]

# Parse trips file
trips_data = []
with open(trips_file, "r") as file:
    lines = file.readlines()
    parsing_trips = False
    
    for line in lines:
        line = line.strip()
        if line == "Trip Sequences:":
            parsing_trips = True
            continue
        
        if parsing_trips and ":" in line:
            trip_id, node_sequence = line.split(": ")
            node_ids = node_sequence.split(", ")
            trip_path = [[nodes[nid][0], nodes[nid][1], i] for i, nid in enumerate(node_ids) if nid in nodes]
            if len(trip_path) > 1:
                trips_data.append({"path": trip_path})

# Generate Pydeck Map
road_layer = pdk.Layer(
    "LineLayer",
    edges,
    get_source_position="start",
    get_target_position="end",
    get_color=[43, 139, 196],  # Blue roads
    get_width=3,
    pickable=False # Disable hover effects
)

bus_marker_layer = pdk.Layer(
    "ScatterplotLayer",
    [{"coordinates": coords, "node_id": node_id} for node_id, coords in bus_nodes.items()],
    get_position="coordinates",
    get_color=[255, 0, 0, 255],  # Red bus stop nodes
    get_radius=4,
    pickable=True,
    tooltip={"text": "{node_id}"}
)

trip_layer = pdk.Layer(
    "TripsLayer",
    trips_data,
    get_path="path",
    get_color=[255, 165, 0],  # Orange for trips
    width_min_pixels=2,
    trail_length=800,  # Longer trail for better animation visibility
    current_time=0,
    pickable=False,
)

# Center map on first bus stop node
if bus_nodes:
    first_bus_node = next(iter(bus_nodes.values()))
    latitude, longitude = first_bus_node[1], first_bus_node[0]
else:
    print("Error: No bus stop nodes found. Terminating program.")
    sys.exit(1)

view_state = pdk.ViewState(
    latitude=latitude,
    longitude=longitude,
    zoom=16,
    pitch=30,
    bearing=0
)

deck = pdk.Deck(
    layers=[road_layer, bus_marker_layer, trip_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",
    tooltip={"html": "<b>Bus Stop Node ID:</b> {node_id}", "style": {"backgroundColor": "steelblue", "color": "white"}}
)

deck.to_html(map_file)
print(f"WebGL Map available at: http://localhost:8080/webgl_map.html")

# Start Local Server
os.system(f"cd {PATH_TO_OSM_FILES} && python -m http.server 8080")