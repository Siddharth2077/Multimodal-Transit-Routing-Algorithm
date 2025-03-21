# import os
# import sys
# import requests
# import folium
# import webbrowser
# import osmium  # Fast OSM parsing
# import platform
# from folium.plugins import FastMarkerCluster
# from folium.plugins import MarkerCluster, FeatureGroupSubGroup

# if __name__ == "__main__":
#     basedir = os.path.dirname(__file__)

#     if platform.system() == "Windows":
#         PATH_TO_OSM_FILES = os.path.join("..", "..", "assets", "osm_files")
#     else:
#         PATH_TO_OSM_FILES = os.path.join("..", "assets", "osm_files")

#     os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)

#     latitude, longitude = 45.5394, -73.6250
#     delta = 0.0045  # Adjusted to a reasonable value (~500m)
#     min_lat, max_lat = latitude - delta, latitude + delta
#     min_lon, max_lon = longitude - delta, longitude + delta

#     osm_file = os.path.join(PATH_TO_OSM_FILES, "map.osm")
#     road_network_file = os.path.join(PATH_TO_OSM_FILES, "road_network.txt")
#     path_file = os.path.join(PATH_TO_OSM_FILES, "path.txt")

#     for file in [road_network_file, path_file]:
#         if not os.path.exists(file):
#             os.open(file, os.O_CREAT)

#     if not os.path.exists(osm_file):
#         osm_url = f"https://overpass-api.de/api/map?bbox={min_lon},{min_lat},{max_lon},{max_lat}"
#         response = requests.get(osm_url)
#         with open(osm_file, 'wb') as file:
#             file.write(response.content)
#         print(f"OSM data saved as '{osm_file}'")

#     class NodeLocationHandler(osmium.SimpleHandler):
#         def __init__(self):
#             super().__init__()
#             self.node_locations = {}

#         def node(self, n):
#             if n.location.valid():
#                 self.node_locations[n.id] = (n.location.lat, n.location.lon)

#     class RoadNetworkHandler(osmium.SimpleHandler):
#         def __init__(self, node_locations):
#             super().__init__()
#             self.node_locations = node_locations
#             self.road_nodes = {}
#             self.road_edges = set()
        
#         def way(self, w):
#             if 'highway' in w.tags:
#                 prev_node_id = None
#                 for node in w.nodes:
#                     if node.ref in self.node_locations:
#                         self.road_nodes[node.ref] = self.node_locations[node.ref]

#                         if prev_node_id is not None:
#                             edge = tuple(sorted([prev_node_id, node.ref]))
#                             self.road_edges.add(edge)

#                         prev_node_id = node.ref

#     node_handler = NodeLocationHandler()
#     node_handler.apply_file(osm_file)

#     road_handler = RoadNetworkHandler(node_handler.node_locations)
#     road_handler.apply_file(osm_file)

#     with open(road_network_file, "w") as file:
#         file.write("Nodes:\n")
#         for node_id, (lat, lon) in road_handler.road_nodes.items():
#             file.write(f"{node_id}: {lat}, {lon}\n")
        
#         file.write("\nEdges:\n")
#         for source, target in sorted(road_handler.road_edges):
#             file.write(f"{source} <-> {target}\n")

#     print(f"Filtered road network saved to {road_network_file}")

#     # Create an interactive Folium map
#     m = folium.Map(
#         location=[latitude, longitude],
#         zoom_start=16,
#         tiles="cartodbpositron",  # Ensures an interactive base map
#         prefer_canvas=True  # Uses GPU for rendering when possible
#     )

#     # Use FastMarkerCluster for better performance
#     marker_cluster = FastMarkerCluster([
#         (lat, lon) for lat, lon in road_handler.road_nodes.values()
#     ], show=False).add_to(m)

#     # Add road edges
#     for source, target in road_handler.road_edges:
#         lat1, lon1 = road_handler.road_nodes[source]
#         lat2, lon2 = road_handler.road_nodes[target]
#         folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="#2B8BC4", weight=1.0).add_to(m)

#     # ! UNCOMMENT THIS BELOW BLOCK TO VIEW NODES IN THE GRAPH
#     # # Add small circle markers for each node with hover tooltips
#     # for node_id, (lat, lon) in road_handler.road_nodes.items():
#     #     folium.CircleMarker(
#     #         location=(lat, lon),
#     #         radius=2,  # Small size
#     #         color="#F848C7",
#     #         fill=True,
#     #         fill_color="#F848C7",
#     #         fill_opacity=1.0,
#     #         tooltip=f"Node ID = {node_id}"  # Shows node ID on hover
#     #     ).add_to(m)



#     # # Create a subgroup for detailed node visualization
#     # node_layer = FeatureGroupSubGroup(marker_cluster, "Nodes").add_to(m)

#     # # Add small circle markers that will appear only when zoomed in
#     # for node_id, (lat, lon) in road_handler.road_nodes.items():
#     #     folium.CircleMarker(
#     #         location=(lat, lon),
#     #         radius=2,  # Small size
#     #         color="#171717",
#     #         fill=True,
#     #         fill_color="#CB274A",
#     #         fill_opacity=1.0,
#     #         tooltip=f"Node ID = {node_id}"  # Shows node ID on hover
#     #     ).add_to(node_layer)

#     # folium.LayerControl().add_to(m)  # Allows toggling layers



#     # Load path if available
#     path_nodes = []
#     if os.path.exists(path_file):
#         with open(path_file, "r") as file:
#             for line in file:
#                 try:
#                     node_id = int(line.strip())
#                     if node_id in road_handler.road_nodes:
#                         path_nodes.append(road_handler.road_nodes[node_id])
#                 except ValueError:
#                     pass

#     # Draw path
#     if len(path_nodes) > 1:
#         folium.PolyLine(
#             path_nodes,
#             color="#313ED1",
#             weight=6,
#             opacity=1.0,
#             tooltip="Optimal Path"
#         ).add_to(m)

#     # Save and open the map
#     map_file = os.path.join(PATH_TO_OSM_FILES, "map.html")
#     m.save(map_file)
#     print(f"Map saved as {map_file}")

#     if platform.system() == "Windows":
#         webbrowser.open(map_file)
#     else:    
#         webbrowser.open("file://" + os.path.abspath(map_file))

import os
import platform
import requests
import osmium
import pydeck as pdk

# Define paths
PATH_TO_OSM_FILES = os.path.join("..", "..", "assets", "osm_files") if platform.system() == "Windows" else os.path.join("..", "assets", "osm_files")
os.makedirs(PATH_TO_OSM_FILES, exist_ok=True)

# Bounding box for OSM data (500m radius)
latitude, longitude = 45.5394, -73.6250
delta = 0.0045
min_lat, max_lat = latitude - delta, latitude + delta
min_lon, max_lon = longitude - delta, longitude + delta

# File path
osm_file = os.path.join(PATH_TO_OSM_FILES, "map.osm")

# Download OSM data if not available
if not os.path.exists(osm_file):
    osm_url = f"https://overpass-api.de/api/map?bbox={min_lon},{min_lat},{max_lon},{max_lat}"
    response = requests.get(osm_url)
    with open(osm_file, "wb") as file:
        file.write(response.content)

# OSM Handlers
class NodeLocationHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.node_locations = {}

    def node(self, n):
        if n.location.valid():
            self.node_locations[n.id] = [n.location.lon, n.location.lat]  # Pydeck uses [lon, lat]

class RoadNetworkHandler(osmium.SimpleHandler):
    def __init__(self, node_locations):
        super().__init__()
        self.node_locations = node_locations
        self.road_edges = []

    def way(self, w):
        if "highway" in w.tags:
            prev_node_id = None
            for node in w.nodes:
                if node.ref in self.node_locations:
                    if prev_node_id is not None:
                        self.road_edges.append({
                            "start": self.node_locations[prev_node_id],
                            "end": self.node_locations[node.ref]
                        })
                    prev_node_id = node.ref

# Parse OSM data
node_handler = NodeLocationHandler()
node_handler.apply_file(osm_file)

road_handler = RoadNetworkHandler(node_handler.node_locations)
road_handler.apply_file(osm_file)

# **Pydeck WebGL Layers**
# Road Layer
road_layer = pdk.Layer(
    "LineLayer",
    road_handler.road_edges,
    get_source_position="start",
    get_target_position="end",
    get_color=[43, 139, 196],  # Blue roads
    get_width=3,
    pickable=True
)

# Marker Layer (Nodes)
marker_layer = pdk.Layer(
    "ScatterplotLayer",
    [{"coordinates": coords} for coords in node_handler.node_locations.values()],
    get_position="coordinates",
    get_color=[255, 0, 0, 200],  # Red markers
    get_radius=1,
)

# **Create Pydeck Map**
view_state = pdk.ViewState(
    latitude=latitude,
    longitude=longitude,
    zoom=16,
    pitch=30,  # 3D effect
    bearing=0
)

deck = pdk.Deck(
    layers=[road_layer, marker_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9"  # Optional: Use Google Maps-like tiles
)

# **Save Map**
map_file = os.path.join(PATH_TO_OSM_FILES, "webgl_map.html")
deck.to_html(map_file)
print(f"WebGL Map available at: http://localhost:8080/webgl_map.html")

# **Start Local Server**
os.system(f"cd {PATH_TO_OSM_FILES} && python -m http.server 8080")


