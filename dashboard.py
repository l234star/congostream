import streamlit as st
import os, json, random
from datetime import datetime
import cloudinary
import cloudinary.uploader

st.set_page_config(page_title="CongoStream Dashboard", layout="wide")

# --- CONNEXION CLOUDINARY AVEC TES SECRETS ---
try:
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloud_name"],
        api_key = st.secrets["cloudinary"]["api_key"],
        api_secret = st.secrets["cloudinary"]["api_secret"]
    )
    st.success("✅ Cloudinary connecté - Tu peux publier Boss!")
except Exception as e:
    st.error(f"❌ Cloudinary non configuré: {e}")
    st.info("Va dans Streamlit > Settings > Secrets et mets tes clés [cloudinary]")
    st.stop()

FILMS_FILE = "films.json"

def charger_films():
    if os.path.exists(FILMS_FILE):
        try:
            with open(FILMS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def sauvegarder_films(films):
    with open(FILMS_FILE, "w", encoding="utf-8") as f:
        json.dump(films, f, indent=2, ensure_ascii=False)

def upload_cloudinary(fichier, dossier):
    if fichier is None:
        return ""
    try:
        resultat = cloudinary.uploader.upload(
            fichier,
            resource_type="auto",
            folder=dossier
        )
        return resultat.get("secure_url", "")
    except Exception as e:
        st.error(f"Erreur upload: {e}")
        return ""

# --- INTERFACE ---
st.title("🎬 CongoStream - Dashboard Boss")

films = charger_films()

with st.form("ajout_film", clear_on_submit=True):
    st.subheader("Publier un nouveau film")
    titre = st.text_input("Titre du film *")
    col1, col2 = st.columns(2)
    with col1:
        genre = st.selectbox("Genre", ["Action", "Comédie", "Drame", "Romantique", "Horreur", "Congolais", "Documentaire"])
        annee = st.number_input("Année", 1990, 2030, 2025)
    with col2:
        description = st.text_area("Description du film")

    st.write("---")
    affiche = st.file_uploader("Affiche du film (Image JPG/PNG)", type=["jpg", "jpeg", "png"])
    video = st.file_uploader("Film complet ou Bande annonce (MP4)", type=["mp4", "mov", "mkv", "avi"])

    publier = st.form_submit_button("🚀 Publier le film")

    if publier:
        if not titre:
            st.warning("Boss, mets le titre!")
        else:
            with st.spinner("Upload en cours vers Cloudinary..."):
                url_image = upload_cloudinary(affiche, "congostream/affiches")
                url_video = upload_cloudinary(video, "congostream/films")

                nouveau = {
                    "id": random.randint(1000, 9999),
                    "titre": titre,
                    "genre": genre,
                    "annee": annee,
                    "desc": description,
                    "image_url": url_image,
                    "trailer_url": url_video,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M")
                }

                films.append(nouveau)
                sauvegarder_films(films)
                st.success(f"Film '{titre}' publié avec succès!")
                st.balloons()
                st.rerun()

st.divider()
st.subheader(f"📚 Films publiés ({len(films)})")

if not films:
    st.info("Aucun film pour l'instant. Publie ton premier Boss!")
else:
    for film in reversed(films):
        with st.expander(f"🎬 {film['titre']} - {film.get('annee','')}"):
            c1, c2 = st.columns([1, 2])
            with c1:
                if film.get("image_url"):
                    st.image(film["image_url"], use_column_width=True)
            with c2:
                st.write(f"**Genre:** {film.get('genre','')}")
                st.write(film.get("desc",""))
                st.write(f"📅 {film.get('date','')}")
                if film.get("trailer_url"):
                    st.video(film["trailer_url"])
