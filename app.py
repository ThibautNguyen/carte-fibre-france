import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import tempfile
import urllib.request

# Chargement des variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Carte de la couverture fibre en France métropolitaine",
    page_icon="🗺️",
    layout="wide"
)

# Titre de l'application
st.title("🗺️ Carte de la couverture fibre en France métropolitaine")

try:
    # Chargement des données
    with st.spinner("Chargement et optimisation des données..."):
        # Téléchargement et chargement des données géographiques
        url = "https://data-interne.ademe.fr/data-fair/api/v1/datasets/geo-contours-communes/data-files/GEO_Contours_Communes.geojson"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Téléchargement du fichier
            json_path = os.path.join(temp_dir, "communes.geojson")
            urllib.request.urlretrieve(url, json_path)
            
            # Lecture du fichier GeoJSON
            communes_gdf = gpd.read_file(json_path)
            
            # Renommer les colonnes pour correspondre à notre structure
            communes_gdf = communes_gdf.rename(columns={
                'DCOE_C_COD': 'insee_com',
                'DCOE_L_LIB': 'nom',
                'DDEP_C_COD': 'dept'
            })
            
            # Filtrer pour garder uniquement la France métropolitaine
            metro_depts = ([f"{i:02d}" for i in range(1, 96)] + ['2A', '2B'])
            communes_gdf = communes_gdf[communes_gdf['dept'].isin(metro_depts)]
        
        # Connexion à la base de données
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        # Chargement des données fibre
        query = "SELECT * FROM reseau.techno_internet_com_2024_clean"
        fibre_df = pd.read_sql(query, conn)
        
        # Fermeture de la connexion
        conn.close()
        
        # Fusion et optimisation des données
        communes_gdf = communes_gdf.merge(
            fibre_df[["code_insee", "pct_fibre", "nb_locaux"]],
            left_on="insee_com",
            right_on="code_insee",
            how="left"
        )
        communes_gdf["pct_fibre"] = communes_gdf["pct_fibre"].fillna(0)
        
    # Création de la carte
    initial_view_state = pdk.ViewState(
        latitude=46.5,
        longitude=2.5,
        zoom=5,
        max_zoom=15,
        pitch=0,
        bearing=0
    )

    def get_fill_color(pct):
        if pd.isna(pct):
            return [200, 200, 200]
        elif pct >= 90:
            return [92, 83, 17]
        elif pct >= 70:
            return [138, 125, 26]
        elif pct >= 50:
            return [184, 166, 35]
        elif pct >= 30:
            return [217, 196, 42]
        elif pct >= 10:
            return [222, 209, 129]
        else:
            return [255, 241, 174]

    communes_gdf["fill_color"] = communes_gdf["pct_fibre"].apply(get_fill_color)

    geojson = pdk.Layer(
        "GeoJsonLayer",
        communes_gdf,
        opacity=0.8,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=True,
        get_fill_color="fill_color",
        get_line_color=[128, 128, 128],
        get_line_width=1,
        pickable=True,
        auto_highlight=True
    )

    r = pdk.Deck(
        layers=[geojson],
        initial_view_state=initial_view_state,
        map_style="light",
        tooltip={
            "html": "<b>{nom}</b><br/>Fibre : {pct_fibre}%",
            "style": {"background": "white", "color": "black", "font-size": "14px", "padding": "5px"}
        }
    )

    st.pydeck_chart(r, height=900)

    # Légende
    st.markdown("""
    <style>
    .legend {
        display: flex;
        align-items: center;
        margin: 10px 0;
        font-size: 14px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        margin-right: 20px;
    }
    .legend-color {
        width: 20px;
        height: 20px;
        margin-right: 5px;
        border: 1px solid #ccc;
    }
    </style>
    <div class="legend">
        <div class="legend-item">
            <div class="legend-color" style="background-color: rgb(92, 83, 17)"></div>
            90-100%
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: rgb(138, 125, 26)"></div>
            70-89%
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: rgb(184, 166, 35)"></div>
            50-69%
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: rgb(217, 196, 42)"></div>
            30-49%
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: rgb(222, 209, 129)"></div>
            10-29%
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: rgb(255, 241, 174)"></div>
            0-9%
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: rgb(200, 200, 200)"></div>
            Données manquantes
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Statistiques
    st.subheader("📊 Statistiques de couverture")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Moyenne nationale",
            f"{communes_gdf['pct_fibre'].mean():.1f}%"
        )
    
    with col2:
        st.metric(
            "Communes 100% fibrées",
            f"{(communes_gdf['pct_fibre'] >= 100).sum():,}"
        )
    
    with col3:
        st.metric(
            "Communes < 50% fibrées",
            f"{(communes_gdf['pct_fibre'] < 50).sum():,}"
        )

except Exception as e:
    st.error(f"Une erreur s'est produite : {str(e)}")
    st.error("Veuillez vérifier la connexion à la base de données et réessayer.") 