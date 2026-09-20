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
    st.success("✅ Cloudinary connecté")
except Exception as e:
    st.error(f"❌ Cloudinary: {e}")
    st.stop()

FILMS_FILE = "films.json"

def charger():
    if os.path.exists(FILMS_FILE):
        try:
            with open(FILMS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

def sauvegarder(films):
    with open(FILMS_FILE, "w", encoding="utf-8") as f:
        json.dump(films, f, indent=2, ensure_ascii=False)

def upload(fichier, dossier):
    if fichier is None: return ""
    try:
        r = cloudinary.uploader.upload(fichier, resource_type="auto", folder=dossier)
        return r.get("secure_url","")
    except Exception as e:
        st.error(f"Erreur {dossier}: {e}")
        return ""

films = charger()

# --- LISTES COMPLÈTES BOSS ---
TYPES = ["Film", "Série", "Série Congolaise", "Série Nollywood", "Telenovela", "Anime", "Court-métrage", "Documentaire", "Spectacle"]

GENRES_COMPLETS = [
    "Action", "Aventure", "Comédie", "Drame", "Romantique", "Horreur", "Thriller", "Suspense",
    "Science-Fiction", "Fantastique", "Policier", "Détective", "Guerre", "Western",
    "Animation", "Anime", "Famille", "Enfant", "Musique", "Danse",
    "Histoire", "Biographie", "Sport", "Documentaire", "Nature",
    "Congolais", "Nollywood", "Africain", "Ivoirien", "Sénégalais",
    "Telenovela", "Bollywood", "Hollywood", "Erotique +18"
]

MOYENS_PAIEMENT = [
    "Gratuit",
    "Location - 500 FCFA / 24h",
    "Location - 1000 FCFA / 48h",
    "Achat - 2000 FCFA",
    "Abonnement Hebdo - 1500 FCFA",
    "Abonnement Mensuel - 5000 FCFA",
    "Premium VIP - 10000 FCFA / mois",
    "MTN Mobile Money",
    "Airtel Money",
    "Orange Money",
    "M-Pesa",
    "Carte Visa / Mastercard"
]

st.title("🎬 CongoStream - Dashboard Boss")

with st.form("ajout_film", clear_on_submit=True):
    st.subheader("Publier un nouveau contenu")
    
    titre = st.text_input("Titre du film / série *")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        type_contenu = st.selectbox("Type", TYPES)
        genre = st.selectbox("Genre principal *", GENRES_COMPLETS)
        annee = st.number_input("Année", 1980, 2030, 2024)
    with col2:
        langue = st.selectbox("Langue", ["Français", "Lingala", "Français + Lingala", "Anglais", "Sous-titré FR", "V.O"])
        duree = st.text_input("Durée / Épisodes", placeholder="Ex: 1h45 ou Saison 1 - 10 épisodes")
        qualite = st.selectbox("Qualité", ["HD 720p", "Full HD 1080p", "4K", "CAM"])
    with col3:
        paiement = st.selectbox("Moyen de paiement / Prix *", MOYENS_PAIEMENT)
        prix = st.text_input("Prix personnalisé", placeholder="Ex: 500 FC")
        age = st.selectbox("Classification", ["Tout public", "-10 ans", "-12 ans", "-16 ans", "-18 ans"])

    description = st.text_area("Synopsis / Description *", height=100)
    
    st.divider()
    st.write("📸 **Médias**")
    c1, c2, c3 = st.columns(3)
    with c1:
        affiche = st.file_uploader("Affiche (Image)", type=["jpg","jpeg","png","webp"])
    with c2:
        bande_annonce = st.file_uploader("Bande Annonce (Vidéo courte)", type=["mp4","mov"])
    with c3:
        film_complet = st.file_uploader("Film / Série COMPLET (Vidéo)", type=["mp4","mov","mkv","avi"])

    publier = st.form_submit_button("🚀 Publier maintenant", use_container_width=True)

    if publier:
        if not titre or not description:
            st.warning("Mets Titre + Description Boss!")
        else:
            with st.spinner("Upload vers Cloudinary..."):
                url_affiche = upload(affiche, "congostream/affiches") if affiche else ""
                url_ba = upload(bande_annonce, "congostream/bandes_annonces") if bande_annonce else ""
                url_film = upload(film_complet, "congostream/films") if film_complet else ""

                nouveau = {
                    "id": random.randint(1000,99999),
                    "titre": titre,
                    "type": type_contenu,
                    "genre": genre,
                    "annee": annee,
                    "langue": langue,
                    "duree": duree,
                    "qualite": qualite,
                    "paiement": paiement,
                    "prix_perso": prix,
                    "classification": age,
                    "desc": description,
                    "image_url": url_affiche,
                    "bande_annonce_url": url_ba,
                    "trailer_url": url_ba,
                    "film_url": url_film,
                    "video_url": url_film if url_film else url_ba,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                films.append(nouveau)
                sauvegarder(films)
                st.success(f"✅ '{titre}' publié! Genre: {genre} | Paiement: {paiement}")
                st.balloons()
                st.rerun()

st.divider()
st.subheader(f"📚 Catalogue ({len(films)} contenus) - Tous genres")

if films:
    # Filtre rapide
    filtre = st.selectbox("Filtrer par genre", ["Tous"] + GENRES_COMPLETS)
    films_filtres = films if filtre=="Tous" else [f for f in films if f.get("genre")==filtre]
    
    for f in reversed(films_filtres):
        with st.expander(f"🎬 {f['titre']} | {f.get('type','Film')} | {f.get('genre','')} | {f.get('paiement','')}"):
            c1, c2 = st.columns([1,2])
            with c1:
                if f.get("image_url"): st.image(f["image_url"], use_container_width=True)
            with c2:
                st.write(f"**Type:** {f.get('type')} | **Genre:** {f.get('genre')} | **Année:** {f.get('annee')}")
                st.write(f"**Qualité:** {f.get('qualite')} | **Langue:** {f.get('langue')} | **Durée:** {f.get('duree')}")
                st.write(f"**💰 Paiement:** {f.get('paiement')} {f.get('prix_perso','')}")
                st.write(f.get("desc",""))
                col_a, col_b = st.columns(2)
                with col_a:
                    if f.get("bande_annonce_url"):
                        st.write("🎥 **Bande Annonce:**")
                        st.video(f["bande_annonce_url"])
                with col_b:
                    if f.get("film_url"):
                        st.write("🎬 **Film Complet:**")
                        st.video(f["film_url"])
