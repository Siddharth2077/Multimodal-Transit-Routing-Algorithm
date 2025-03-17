# import requests
# import os
# import glob
# import osmnx as ox
# import folium

# # 45.5394N, 73.6250W

# PATH_TO_OSM_FILES = os.path.abspath(os.path.join("..", "..", "assets", "osm_files"))


# def download_osm_map(center_lat, center_lon, output_dir, filename="map.osm"):
#     """
#     Downloads a 500m x 500m OSM map centered at the given coordinates and saves it to a file.
    
#     Parameters:
#         center_lat (float): Latitude of the center point.
#         center_lon (float): Longitude of the center point.
#         output_dir (str): Path to the directory where the OSM file should be saved.
#         filename (str): Name of the output file (default: "map.osm").
    
#     Returns:
#         str: Path to the downloaded OSM file, or None if the download fails.
#     """
#     OFFSET = 0.00225  # Approximate 500m offset in degrees (1 degree ≈ 111km)

#     # Compute bounding box (left, bottom, right, top)
#     bbox = f"{center_lon - OFFSET},{center_lat - OFFSET},{center_lon + OFFSET},{center_lat + OFFSET}"

#     # Overpass API query
#     query = f"""
#     [out:xml];
#     (
#       node({bbox});
#       way({bbox});
#       relation({bbox});
#     );
#     (._;>;);
#     out meta;
#     """

#     # Ensure output directory exists
#     os.makedirs(output_dir, exist_ok=True)
#     output_file = os.path.join(output_dir, filename)

#     # Send request to Overpass API
#     overpass_url = "https://overpass-api.de/api/interpreter"
#     response = requests.post(overpass_url, data={"data": query})

#     # Save OSM data to file if successful
#     if response.status_code == 200:
#         with open(output_file, "w", encoding="utf-8") as file:
#             file.write(response.text)
#         print(f"✅ OSM map saved to: {output_file}")
#         return output_file
#     else:
#         print(f"❌ Failed to fetch data: {response.status_code}")
#         return None


# def visualize_osm_file():
#     # Define file path
#     # osm_file = download_osm_map(45.5394, -73.6250, PATH_TO_OSM_FILES, "montreal_500m.osm")

#     osm_file = os.path.join(PATH_TO_OSM_FILES, "montreal_500m.osm")

#     # Load OSM data into a graph using the correct function
#     G = ox.graph_from_xml(osm_file, simplify=True)

#     # Convert graph to GeoDataFrames
#     nodes, edges = ox.graph_to_gdfs(G)

#     # Get the centroid of all nodes
#     center = nodes.geometry.unary_union.centroid

#     # Create a folium map centered at the graph location
#     m = folium.Map(location=[center.y, center.x], zoom_start=15)

#     # Plot edges on the map
#     for _, edge in edges.iterrows():
#         if edge.geometry is not None:  # Ensure the edge has geometry data
#             points = [(point[1], point[0]) for point in edge.geometry.coords]
#             folium.PolyLine(points, color="blue", weight=2.5, opacity=0.8).add_to(m)

#     # Save and display the map
#     map_file = "osm_visualization.html"
#     m.save(map_file)
#     print(f"✅ Map saved as {map_file}. Open it in a browser.")


# # MAIN
# # ! REMOVE THIS LATER
# if __name__ == "__main__":
#     visualize_osm_file()


import requests
import folium
import webbrowser
from IPython.display import display

if __name__ == "__main__":
    # Coordinates and bounding box size
    latitude, longitude = 45.5394, -73.6250
    delta = 0.00225  # Approx 500m in degrees

    # Download OSM data
    osm_url = f"https://overpass-api.de/api/map?bbox={longitude-delta},{latitude-delta},{longitude+delta},{latitude+delta}"
    osm_file = "map.osm"

    response = requests.get(osm_url)
    with open(osm_file, 'wb') as file:
        file.write(response.content)

    print(f"OSM data saved as '{osm_file}'")

    # Create and save the Folium map
    m = folium.Map(location=[latitude, longitude], zoom_start=16)
    folium.Marker([latitude, longitude], popup="Center Point").add_to(m)

    map_file = "map.html"
    m.save(map_file)
    print(f"Map saved as {map_file}")

    # Open in browser
    webbrowser.open(map_file)


