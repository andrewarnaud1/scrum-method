import pandas as pd
import folium
from folium.plugins import MarkerCluster
import sqlite3

# Créez la carte de base
m = folium.Map(location=[48.86762, 2.3624], tiles="OpenStreetMap", zoom_start=5)

conn = sqlite3.connect("db.sqlite3")  # Replace with your actual database file
print(conn)

# Read data from the database
query = "SELECT * FROM restaurants"  # Adjust your SQL query as needed
df = pd.read_sql_query(query, conn)

# Créez un groupe de marqueurs
marker_cluster = MarkerCluster().add_to(m)

for i, row in df.iterrows():
    lat = df.at[i, "lat"]
    lng = df.at[i, "lng"]
    restaurant = df.at[i, "restaurant"]
    street = str(df.at[i, "street"])
    zip_code = str(df.at[i, "zip"])

    # Créez le texte de la popup avec un lien de réservation
    popup_text = f"""
    <b>{restaurant}</b><br>
    {street}<br>
    {zip_code}<br>
    <a href="https://www.facebook.com/login.php">Faire une réservation</a>
    """

    if restaurant == "McDonalds":
        color = "blue"
    else:
        color = "red"

    # Créez un marqueur personnalisé avec la popup
    marker = folium.Marker(
        location=[lat, lng],
        icon=folium.DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html=f'<div><span style="color: {color}; font-size: 12pt;">{restaurant}</span></div>',
        ),
    )
    marker.add_to(marker_cluster)

    # Ajoutez la popup à côté du marqueur
    folium.Popup(popup_text).add_to(marker)

m.save("templates/map.html")
