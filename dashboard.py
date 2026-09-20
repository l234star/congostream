import streamlit as st
import os, json, random
from datetime import datetime
import cloudinary
import cloudinary.uploader

st.set_page_config(page_title="CongoStream Dashboard", layout="wide")

try:
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloud_name"],
        api_key = st.secrets["cloudinary"]["api_key"],
        api_secret = st.secrets["cloudinary"]["api_secret"]
    )
    st.success("✅ Cloudinary OK - Prêt à publier")
except Exception as e:
    st.error(f"❌ Erreur Cloudinary: {e}")
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

def enregistrer_films(films):
    with open(FILMS_FILE, "w", encoding="utf-8") as f:
        json.dump(films, f, indent=2, ensure_ascii=False)

def upload_cloud(file, folder):
    if file is None:
        return ""
    try:
        result = cloudinary.uploader.upload(file, resource_type="auto", folder=folder)
        return result.get("secure_url", "")
    except Exception as e:
        st.error(f"Erreur upload {folder}: {e}")
        return ""

# --- LISTES COMPLÈTES ---
GENRES_COMPLETS = [
    "Action", "Aventure", "Comédie", "Drame", "Romantique", "Horreur", "Thriller", "Suspense",
    "Science-Fiction", "Fantastique", "Policier", "Guerre", "Western", "Animation", "Anime",
    "Famille", "Musique", "Histoire", "Biographie", "Sport", "Documentaire",
    "Congolais", "Nollywood", "Africain", "Ivoirien", "Sénégalais", "Telenovela", "Bollywood"
]

TYPES_CONTENU = ["Film", "Série", "Série Congolaise", "Nollywood", "Telenovela", "Anime", "Documentaire", "Court-métrage"]

MOYENS_PAIEMENT = [
    "Gratuit",
    "Location 500 FCFA / 24h",
    "Location 1000 FCFA / 48h", 
    "Achat 2000 FCFA",
    "Abonnement Hebdo 1500 FCFA",
    "Abonnement Mensuel 5000 FCFA",
    "Premium VIP 10000 FCFA",
    "MTN Mobile Money",
    "Airtel Money", 
    "Orange Money",
    "M-Pesa"
]

films = charger_films()

st.title("🎬 CongoStream - Dashboard Boss")

# ===== PARTIE PUBLICATION (Interface que tu aimes) =====
with st.form("ajout_film", clear_on_submit=True):
    st.subheader("Ajouter un film")
    col1, col2 = st.columns(2)
    with col1:
        titre = st.text_input("Titre du film *")
        type_film = st.selectbox("Type", TYPES_CONTENU)
        genre = st.selectbox("Genre *", GENRES_COMPLETS)
        annee = st.number_input("Année", 1990, 2030, 2024)
    with col2:
        desc = st.text_area("Description")
        paiement = st.selectbox("Moyen de paiement / Prix *", MOYENS_PAIEMENT)
        prix_perso = st.text_input("Prix personnalisé (optionnel)", placeholder="Ex: 500 FC")
        qualite = st.selectbox("Qualité", ["HD 720p", "Full HD 1080p", "4K"])

    st.divider()
    st.write("📸 **Médias - 3 uploads**")
    c1, c2, c3 = st.columns(3)
    with c1:
        image_file = st.file_uploader("Affiche (image)", type=["jpg","png","jpeg","webp"])
    with c2:
        bande_annonce_file = st.file_uploader("Bande Annonce", type=["mp4","mov"])
    with c3:
        film_file = st.file_uploader("Film complet", type=["mp4","mov","avi","mkv"])

    submitted = st.form_submit_button("🚀 Publier le film")

    if submitted:
        if not titre:
            st.error("Mets le titre Boss!")
        else:
            with st.spinner("Upload en cours..."):
                image_url = upload_cloud(image_file, "congostream/affiches") if image_file else ""
                ba_url = upload_cloud(bande_annonce_file, "congostream/ba") if bande_annonce_file else ""
                film_url = upload_cloud(film_file, "congostream/films") if film_file else ""

                # On garde compatibilité avec ancien code: trailer_url + film_url + bande_annonce_url
                nouveau_film = {
                    "id": random.randint(1000,9999),
                    "titre": titre,
                    "type": type_film,
                    "genre": genre,
                    "annee": annee,
                    "desc": desc,
                    "paiement": paiement,
                    "prix_perso": prix_perso,
                    "qualite": qualite,
                    "image_url": image_url,
                    "bande_annonce_url": ba_url,
                    "trailer_url": ba_url,  # pour ancien code
                    "film_url": film_url,
                    "video_url": film_url if film_url else ba_url,
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                films.append(nouveau_film)
                enregistrer_films(films)
                st.success(f"Le film '{titre}' apparait maintenant! ✅")
                st.balloons()
                st.rerun()

# ===== PARTIE LECTURE DES CONTENUS (COMME AVANT - REMIS) =====
st.divider()
st.subheader(f"📚 Films enregistrés ({len(films)}) - Lecture")

if len(films) == 0:
    st.info("Aucun film enregistré pour le moment Boss!")
else:
    for film in reversed(films):
        with st.expander(f"{film['titre']} - {film['annee']} - {film.get('genre','')} - {film.get('paiement','Gratuit')}"):
            c1, c2 = st.columns([1,2])
            with c1:
                if film.get("image_url"):
                    st.image(film["image_url"], width=200)
                st.write(f"**Genre:** {film.get('genre','')}")
                st.write(f"**Type:** {film.get('type','Film')}")
                st.write(f"**💰 Prix:** {film.get('paiement','')} {film.get('prix_perso','')}")
                st.write(f"**Qualité:** {film.get('qualite','')}")
            with c2:
                st.write(f"**Description:** {film.get('desc','')}")
                st.write(f"**Date:** {film.get('timestamp','')}")
                
                # Bande annonce
                ba = film.get("bande_annonce_url") or film.get("trailer_url")
                if ba:
                    st.write("🎥 **Bande Annonce:**")
                    st.video(ba)
                
                # Film complet
                vf = film.get("film_url") or film.get("video_url")
                if vf and vf != ba:
                    st.write("🎬 **Film Complet:**")
                    st.video(vf)
                elif vf and not ba:
                    st.write("🎬 **Vidéo:**")
                    st.video(vf)
