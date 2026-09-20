import streamlit as st
import os, json, random
from datetime import datetime
import cloudinary
import cloudinary.uploader

st.set_page_config(page_title="CongoStream", layout="wide", page_icon="🎬")

st.markdown("""
<style>
.congo-header {
    background: linear-gradient(to bottom, #000000 0%, #141414 100%);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}
.congo-title {
    color: #E50914;
    font-size: 40px;
    font-weight: 900;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

try:
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloud_name"],
        api_key = st.secrets["cloudinary"]["api_key"],
        api_secret = st.secrets["cloudinary"]["api_secret"]
    )
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
def upload(file, folder):
    if not file: return ""
    try:
        r = cloudinary.uploader.upload(file, resource_type="auto", folder=folder)
        return r.get("secure_url","")
    except Exception as e:
        st.error(f"Upload {folder}: {e}")
        return ""

GENRES = ["Action","Aventure","Comédie","Drame","Romantique","Horreur","Thriller","Science-Fiction","Fantastique","Policier","Animation","Anime","Famille","Congolais","Nollywood","Africain","Telenovela","Documentaire","Bollywood"]
TYPES = ["Film","Série","Série Congolaise","Nollywood","Telenovela","Anime","Documentaire"]
PAIEMENTS = ["Gratuit","Location 500 FCFA / 24h","Location 1000 FCFA / 48h","Achat 2000 FCFA","Abonnement Hebdo 1500 FCFA","Abonnement Mensuel 5000 FCFA","Premium VIP 10000 FCFA","MTN Mobile Money","Airtel Money","Orange Money","M-Pesa"]

films = charger()

# ===== HEADER CORRIGÉ By.Mr_Joksan =====
st.markdown('<div class="congo-header"><span class="congo-title">CONGOSTREAM</span> <span style="color:white; margin-left:20px; font-size:18px;">By.Mr_Joksan</span></div>', unsafe_allow_html=True)

# Onglets corrigés sans Netflix
tab1, tab2 = st.tabs(["🏠 ACCUEIL", "➕ PUBLIER UN FILM"])

with tab1:
    if films:
        dernier = films[-1]
        col1, col2 = st.columns([2,1])
        with col1:
            if dernier.get("image_url"):
                st.image(dernier["image_url"], use_container_width=True)
        with col2:
            st.markdown(f"### 🎬 {dernier['titre']}")
            st.write(f"**{dernier.get('genre','')}** • {dernier.get('annee','')} • {dernier.get('qualite','HD')}")
            st.write(dernier.get('desc',''))
            st.write(f"💰 **{dernier.get('paiement','Gratuit')}**")
            if dernier.get("bande_annonce_url") or dernier.get("trailer_url"):
                st.video(dernier.get("bande_annonce_url") or dernier.get("trailer_url"))
    else:
        st.info("Aucun film - Publie ton premier dans l'onglet PUBLIER UN FILM!")

    st.divider()
    st.subheader(f"📚 Catalogue complet ({len(films)} films)")
    
    if films:
        recherche = st.text_input("🔍 Rechercher", placeholder="Titre, genre...")
        films_filtres = [f for f in films if recherche.lower() in f['titre'].lower() or recherche.lower() in f.get('genre','').lower()] if recherche else films
        cols = st.columns(4)
        for idx, film in enumerate(reversed(films_filtres)):
            with cols[idx % 4]:
                with st.container(border=True):
                    if film.get("image_url"):
                        st.image(film["image_url"], use_container_width=True)
                    st.write(f"**{film['titre']}**")
                    st.caption(f"{film.get('genre','')} • {film.get('annee','')} | {film.get('paiement','')}")
                    with st.expander("▶ Voir"):
                        st.write(film.get("desc",""))
                        if film.get("bande_annonce_url"):
                            st.write("🎥 Bande Annonce")
                            st.video(film["bande_annonce_url"])
                        if film.get("film_url"):
                            st.write("🎬 Film Complet")
                            st.video(film["film_url"])
    else:
        st.write("Catalogue vide")

with tab2:
    st.subheader("Publier un nouveau film")
    with st.form("ajout_film", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            titre = st.text_input("Titre du film *")
            type_film = st.selectbox("Type", TYPES)
            genre = st.selectbox("Genre *", GENRES)
            annee = st.number_input("Année", 1990, 2030, 2024)
        with col2:
            desc = st.text_area("Description *", height=100)
            paiement = st.selectbox("Moyen de paiement / Prix *", PAIEMENTS)
            prix_perso = st.text_input("Prix perso", placeholder="500 FC")
            qualite = st.selectbox("Qualité", ["HD 720p","Full HD 1080p","4K"])

        st.divider()
        st.write("📸 Médias")
        c1, c2, c3 = st.columns(3)
        with c1:
            img = st.file_uploader("Affiche", type=["jpg","jpeg","png","webp"])
        with c2:
            ba = st.file_uploader("Bande Annonce", type=["mp4","mov"])
        with c3:
            film_f = st.file_uploader("Film complet", type=["mp4","mov","mkv","avi"])

        btn = st.form_submit_button("🚀 Publier le film", use_container_width=True)
        if btn:
            if not titre:
                st.error("Mets le titre!")
            else:
                with st.spinner("Upload Cloudinary..."):
                    url_img = upload(img, "congostream/affiches")
                    url_ba = upload(ba, "congostream/ba")
                    url_film = upload(film_f, "congostream/films")
                    nouveau = {
                        "id": random.randint(1000,99999),
                        "titre": titre, "type": type_film, "genre": genre, "annee": annee,
                        "desc": desc, "paiement": paiement, "prix_perso": prix_perso, "qualite": qualite,
                        "image_url": url_img, "bande_annonce_url": url_ba, "trailer_url": url_ba,
                        "film_url": url_film, "video_url": url_film if url_film else url_ba,
                        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
                    }
                    films.append(nouveau)
                    sauvegarder(films)
                    st.success(f"✅ '{titre}' publié!")
                    st.balloons()
                    st.rerun()
