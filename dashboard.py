import streamlit as st
import os, json, random
from datetime import datetime
import cloudinary
import cloudinary.uploader

st.set_page_config(page_title="CongoStream", layout="wide", page_icon="🎬")

# --- CONFIG SECRÈTE ---
CODE_ADMIN = "JOKSAN2026"  # <- TON CODE POUR PUBLIER ET GÉRER
NUMERO_PAIEMENT = "066778924"

st.markdown("""
<style>
.congo-header { background: #000; padding: 20px; border-radius: 10px; margin-bottom:20px; }
.congo-title { color: #E50914; font-size: 40px; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

try:
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloud_name"],
        api_key = st.secrets["cloudinary"]["api_key"],
        api_secret = st.secrets["cloudinary"]["api_secret"]
    )
except: st.stop()

FILMS_FILE = "films.json"
TRANSAC_FILE = "transactions.json"

def charger(nom):
    if os.path.exists(nom):
        try:
            with open(nom,"r",encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

def sauvegarder(nom, data):
    with open(nom,"w",encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def upload(file, folder):
    if not file: return ""
    try:
        r = cloudinary.uploader.upload(file, resource_type="auto", folder=folder)
        return r.get("secure_url","")
    except Exception as e:
        st.error(f"Erreur: {e}")
        return ""

GENRES = ["Action","Aventure","Comédie","Drame","Romantique","Horreur","Thriller","Science-Fiction","Fantastique","Policier","Animation","Anime","Famille","Congolais","Nollywood","Africain","Telenovela","Documentaire","Bollywood"]
TYPES = ["Film","Série","Série Congolaise","Nollywood","Telenovela","Anime","Documentaire"]
PAIEMENTS = ["Gratuit","Location 500 FCFA / 24h","Location 1000 FCFA / 48h","Achat 2000 FCFA","Abonnement Hebdo 1500 FCFA","Abonnement Mensuel 5000 FCFA","Premium VIP 10000 FCFA","MTN Mobile Money","Airtel Money","Orange Money","M-Pesa"]

films = charger(FILMS_FILE)
transactions = charger(TRANSAC_FILE)

st.markdown(f'<div class="congo-header"><span class="congo-title">CONGOSTREAM</span> <span style="color:white; margin-left:20px;">By.Mr_Joksan</span></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏠 ACCUEIL", "➕ PUBLIER", "⚙️ GÉRER LES CONTENUS"])

# ================= ACCUEIL =================
with tab1:
    st.subheader(f"Catalogue ({len(films)} films)")
    if films:
        recherche = st.text_input("🔍 Rechercher", placeholder="Titre, genre...")
        liste = [f for f in films if recherche.lower() in f['titre'].lower()] if recherche else films
        cols = st.columns(4)
        for idx, film in enumerate(reversed(liste)):
            with cols[idx % 4]:
                with st.container(border=True):
                    if film.get("image_url"): st.image(film["image_url"], use_container_width=True)
                    st.write(f"**{film['titre']}**")
                    st.caption(f"{film.get('genre','')} | {film.get('paiement','Gratuit')}")
                    with st.expander("▶ Voir"):
                        st.write(film.get("desc",""))
                        # Si payant
                        if film.get("paiement") != "Gratuit":
                            st.warning(f"🔒 Film payant: {film.get('paiement')}")
                            st.info(f"1️⃣ Envoie l'argent au **{NUMERO_PAIEMENT}**\n\n2️⃣ Envoie l'ID de transaction ci-dessous\n\n3️⃣ Attends 5 min max pour confirmation")
                            id_transac = st.text_input(f"ID transaction pour {film['id']}", key=f"trans_{film['id']}")
                            if st.button(f"Envoyer ID", key=f"btn_{film['id']}"):
                                transactions.append({"film_id":film['id'],"titre":film['titre'],"id_transaction":id_transac,"statut":"En attente","date":datetime.now().strftime("%d/%m %H:%M")})
                                sauvegarder(TRANSAC_FILE, transactions)
                                st.success("ID envoyé! Attends 5 min, l'associé va confirmer.")
                        # Vidéos
                        if film.get("bande_annonce_url"):
                            st.write("🎥 Bande Annonce")
                            st.video(film["bande_annonce_url"])
                        if film.get("paiement")=="Gratuit" and film.get("film_url"):
                            st.write("🎬 Film Complet")
                            st.video(film["film_url"])
    else:
        st.info("Catalogue vide")

# ================= PUBLIER (AVEC CODE) =================
with tab2:
    st.subheader("Zone Admin - Publier")
    code = st.text_input("Entre ton code admin pour publier", type="password")
    if code != CODE_ADMIN:
        st.warning("🔐 Entre le code secret pour accéder à la publication")
        st.stop()
    
    st.success("✅ Accès autorisé By.Mr_Joksan")
    with st.form("ajout_film", clear_on_submit=True):
        c1,c2 = st.columns(2)
        with c1:
            titre = st.text_input("Titre *")
            type_f = st.selectbox("Type", TYPES)
            genre = st.selectbox("Genre", GENRES)
            annee = st.number_input("Année",1990,2030,2024)
        with c2:
            desc = st.text_area("Description *")
            paiement = st.selectbox("Prix / Paiement *", PAIEMENTS)
            prix_perso = st.text_input("Prix perso")
            qualite = st.selectbox("Qualité", ["HD 720p","Full HD 1080p","4K"])
        st.divider()
        f1,f2,f3 = st.columns(3)
        with f1: img = st.file_uploader("Affiche", type=["jpg","jpeg","png","webp"])
        with f2: ba = st.file_uploader("Bande Annonce", type=["mp4","mov"])
        with f3: film_f = st.file_uploader("Film complet", type=["mp4","mov","mkv","avi"])
        btn = st.form_submit_button("🚀 Publier", use_container_width=True)
        if btn and titre:
            with st.spinner("Upload..."):
                url_img = upload(img,"congostream/affiches")
                url_ba = upload(ba,"congostream/ba")
                url_film = upload(film_f,"congostream/films")
                films.append({
                    "id":random.randint(1000,99999),"titre":titre,"type":type_f,"genre":genre,"annee":annee,
                    "desc":desc,"paiement":paiement,"prix_perso":prix_perso,"qualite":qualite,
                    "image_url":url_img,"bande_annonce_url":url_ba,"trailer_url":url_ba,
                    "film_url":url_film,"video_url":url_film if url_film else url_ba,
                    "timestamp":datetime.now().strftime("%d/%m/%Y %H:%M")
                })
                sauvegarder(FILMS_FILE, films)
                st.success(f"✅ {titre} publié!")
                st.balloons()
                st.rerun()

# ================= GÉRER LES CONTENUS (AVEC CODE) =================
with tab3:
    st.subheader("⚙️ Gestion des contenus + Validation paiements")
    code2 = st.text_input("Code admin pour gérer", type="password", key="code_gerer")
    if code2 != CODE_ADMIN:
        st.warning("🔐 Code requis pour gérer les contenus")
        st.stop()
    
    st.success("✅ Mode Gestion activé")
    
    # Partie 1: Validation des paiements
    st.write("### 💰 Transactions en attente")
    if transactions:
        for t in transactions:
            c1,c2,c3,c4 = st.columns([2,2,2,1])
            with c1: st.write(f"🎬 {t['titre']}")
            with c2: st.write(f"ID: {t['id_transaction']}")
            with c3: st.write(f"Statut: {t['statut']} - {t['date']}")
            with c4:
                if st.button("Confirmer", key=f"conf_{t['id_transaction']}"):
                    t['statut']="Confirmé"
                    sauvegarder(TRANSAC_FILE, transactions)
                    st.success("Confirmé!")
                    st.rerun()
                if st.button("Suppr", key=f"del_{t['id_transaction']}"):
                    transactions.remove(t)
                    sauvegarder(TRANSAC_FILE, transactions)
                    st.rerun()
    else:
        st.info("Aucune transaction")

    st.divider()
    st.write(f"### 📚 Gérer les films ({len(films)})")
    for film in reversed(films):
        with st.expander(f"{film['titre']} - {film.get('paiement','')}"):
            c1,c2 = st.columns([1,3])
            with c1:
                if film.get("image_url"): st.image(film["image_url"], width=150)
            with c2:
                st.write(f"Genre: {film.get('genre')} | {film.get('type')}")
                st.write(film.get("desc",""))
                if st.button(f"🗑️ Supprimer {film['titre']}", key=f"sup_{film['id']}"):
                    films = [f for f in films if f['id']!=film['id']]
                    sauvegarder(FILMS_FILE, films)
                    st.warning(f"{film['titre']} supprimé")
                    st.rerun()
