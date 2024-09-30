# import folium


# def base():
#     # this is base map
#     map = folium.Map(location=[45.52336, -122.6750])

#     file = open("./templates/maps.html", "w")
#     return file.write(map)


# @app.route("/open-street-map")
# def open_street_map():
#     # this map using stamen toner
#     map = folium.Map(
#         location=[45.52336, -122.6750], tiles="Stamen Toner", zoom_start=13
#     )

#     folium.Marker(
#         location=[45.52336, -122.6750],
#         popup="<b>Marker here</b>",
#         tooltip="Click Here!",
#     ).add_to(map)

#     return map._repr_html_()


# @app.route("/map-marker")
# def map_marker():
#     # this map using stamen terrain
#     # we add some marker here
#     map = folium.Map(
#         location=[45.52336, -122.6750], tiles="Stamen Terrain", zoom_start=12
#     )

#     folium.Marker(
#         location=[45.52336, -122.6750],
#         popup="<b>Marker here</b>",
#         tooltip="Click Here!",
#     ).add_to(map)

#     folium.Marker(
#         location=[45.55736, -122.8750],
#         popup="<b>Marker 2 here</b>",
#         tooltip="Click Here!",
#         icon=folium.Icon(color="green"),
#     ).add_to(map)

#     folium.Marker(
#         location=[45.53236, -122.8750],
#         popup="<b>Marker 3 here</b>",
#         tooltip="Click Here!",
#         icon=folium.Icon(color="red"),
#     ).add_to(map)

#     return map._repr_html_()


# if __name__ == "__main__":
#     app.run(debug=True)
