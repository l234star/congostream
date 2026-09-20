import streamlit as st
import os, json, random
from datetime import datetime
import cloudinary
import cloudinary.uploader

st.set_page_config(page_title="CongoStream", layout="wide", page_icon="🎬")

CODE_ADMIN = "JOKSAN2026"
NUMERO_PAIEMENT = "066778924"

st.markdown("""
<style>
.congo-header { background: #000; padding: 20px; border-radius: 10px; margin-bottom:20px; }
.congo-title { color: #E50914; font-size: 38px; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

try:
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloud_name"],
        api_key = st.secrets["cloudinary"]["api_key"],
        api_secret = st.secrets["cloudinary"]["api_secret"]
    )
    cloudinary_ok = True
except:
    cloudinary_ok = False

FILMS_FILE = "films.json"
TRANSAC_FILE = "transactions.json"

def charger(nom):
    if os.path.exists(nom):
        try:
            with open(nom,"r",encoding="utf-8") as f: 
                data = json.load(f)
                return data if isinstance(data, list) else []
        except: 
            return []
    return []

def sauvegarder(nom, data):
    with open(nom,"w",encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def upload(file, folder):
    if not file: 
        return ""
    if not cloudinary_ok:
        st.error("Cloudinary non connecté")
        return ""
    try:
        # Pour vidéo on force bien
        r = cloudinary.uploader.upload(file, resource_type="auto", folder=folder, chunk_size=6000000)
        return r.get("secure_url","")
    except Exception as e:
        st.error(f"Erreur upload: {e}")
        return ""

# Charge les films
if "films" not in st.session_state:
    st.session_state.films = charger(FILMS_FILE)
if "trans" not in st.session_state:
    st.session_state.trans = charger(TRANSAC_FILE)

films = st.session_state.films

st.markdown(f'<div class="congo-header"><span class="congo-title">CONGOSTREAM</span> <span style="color:white; margin-left:20px;">By.Mr_Joksan</span> <span style="color:gray; float:right;">{"✅ Cloudinary OK" if cloudinary_ok else "❌ Cloudinary HS"}</span></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏠 ACCUEIL", "➕ PUBLIER", "⚙️ GÉRER"])

# ================= ACCUEIL - LECTURE CORRIGÉE =================
with tab1:
    st.subheader(f"📚 Catalogue ({len(films)} films publiés)")
    
    if not films:
        st.info("Catalogue vide pour l'instant. Publie un film dans l'onglet PUBLIER!")
        st.write(f"Fichier films.json existe? {os.path.exists(FILMS_FILE)}")
    else:
        # Recherche
        recherche = st.text_input("🔍 Rechercher", placeholder="Titre...")
        liste = [f for f in films if recherche.lower() in f['titre'].lower()] if recherche else films
        
        # AFFICHAGE GRILLE
        cols = st.columns(3)
        for idx, film in enumerate(reversed(liste)):
            with cols[idx % 3]:
                with st.container(border=True):
                    if film.get("image_url"):
                        st.image(film["image_url"], use_container_width=True)
                    else:
                        st.write("🖼️ Pas d'affiche")
                    
                    st.markdown(f"**{film['titre']}**")
                    st.caption(f"{film.get('genre','')} • {film.get('annee','')} • {film.get('paiement','Gratuit')}")
                    
                    # BOUTON LECTURE DIRECT
                    if film.get("bande_annonce_url"):
                        st.video(film["bande_annonce_url"])
                    
                    # Si gratuit, on montre le film direct
                    if film.get("paiement") == "Gratuit":
                        if film.get("film_url"):
                            with st.expander("▶ Voir film complet gratuit"):
                                st.video(film["film_url"])
                    else:
                        # Payant
                        with st.expander(f"🔒 Payant - {film.get('paiement')} - Débloquer"):
                            st.warning(f"Envoie {film.get('paiement')} au **{NUMERO_PAIEMENT}**")
                            st.write("Ensuite envoie l'ID de transaction:")
                            id_trans = st.text_input("ID Transaction", key=f"pay_{film['id']}")
                            if st.button("Envoyer", key=f"send_{film['id']}"):
                                st.session_state.trans.append({
                                    "film_id":film['id'],"titre":film['titre'],
                                    "id_transaction":id_trans,"statut":"En attente",
                                    "date":datetime.now().strftime("%d/%m %H:%M")
                                })
                                sauvegarder(TRANSAC_FILE, st.session_state.trans)
                                st.success("ID envoyé! Attends 5min max, l'associé va confirmer.")
                            
                            # Si déjà confirmé, on montre
                            # (ici on vérifie si transaction confirmée)
                            for t in st.session_state.trans:
                                if t['film_id']==film['id'] and t['statut']=="Confirmé":
                                    st.success("✅ Paiement confirmé!")
                                    if film.get("film_url"):
                                        st.video(film["film_url"])

# ================= PUBLIER =================
with tab2:
    st.subheader("Publier - Accès sécurisé")
    code = st.text_input("Code admin", type="password", key="code_pub")
    
    if code == CODE_ADMIN:
        st.success("Accès autorisé")
        with st.form("form_pub", clear_on_submit=True):
            c1,c2 = st.columns(2)
            with c1:
                titre = st.text_input("Titre *")
                type_f = st.selectbox("Type", ["Film","Série","Série Congolaise","Nollywood","Telenovela","Anime","Documentaire"])
                genre = st.selectbox("Genre", ["Action","Aventure","Comédie","Drame","Romantique","Horreur","Thriller","Science-Fiction","Congolais","Nollywood","Africain","Telenovela","Documentaire"])
                annee = st.number_input("Année",1990,2030,2024)
            with c2:
                desc = st.text_area("Description *")
                paiement = st.selectbox("Paiement", ["Gratuit","Location 500 FCFA / 24h","Location 1000 FCFA / 48h","Achat 2000 FCFA","Abonnement Mensuel 5000 FCFA","MTN Mobile Money","Airtel Money","Orange Money"])
                prix = st.text_input("Prix perso")
                qualite = st.selectbox("Qualité", ["HD 720p","Full HD 1080p","4K"])
            
            f1,f2,f3 = st.columns(3)
            with f1: img = st.file_uploader("Affiche", type=["jpg","jpeg","png","webp"])
            with f2: ba = st.file_uploader("Bande annonce", type=["mp4","mov"])
            with f3: film_f = st.file_uploader("Film complet", type=["mp4","mov","mkv","avi"])
            
            btn = st.form_submit_button("🚀 Publier", use_container_width=True)
            if btn:
                if not titre:
                    st.error("Titre obligatoire")
                else:
                    with st.spinner("Upload..."):
                        url_img = upload(img, "congostream/affiches")
                        url_ba = upload(ba, "congostream/ba")
                        url_film = upload(film_f, "congostream/films")
                        
                        nouveau = {
                            "id": random.randint(1000,99999),
                            "titre": titre, "type": type_f, "genre": genre, "annee": annee,
                            "desc": desc, "paiement": paiement, "prix_perso": prix, "qualite": qualite,
                            "image_url": url_img, "bande_annonce_url": url_ba, "trailer_url": url_ba,
                            "film_url": url_film, "video_url": url_film if url_film else url_ba,
                            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
                        }
                        st.session_state.films.append(nouveau)
                        sauvegarder(FILMS_FILE, st.session_state.films)
                        st.success(f"✅ {titre} publié et visible dans ACCUEIL!")
                        st.balloons()
    elif code != "":
        st.error("Code faux")

# ================= GÉRER =================
with tab3:
    st.subheader("Gérer les contenus")
    code2 = st.text_input("Code admin", type="password", key="code_gerer")
    if code2 == CODE_ADMIN:
        st.write(f"### 💰 Transactions ({len(st.session_state.trans)})")
        for t in st.session_state.trans:
            c1,c2,c3,c4 = st.columns([2,2,2,1])
            c1.write(t['titre']); c2.write(t['id_transaction']); c3.write(t['statut'])
            if c4.button("Confirmer", key=f"c_{t['id_transaction']}_{t['film_id']}"):
                t['statut']="Confirmé"
                sauvegarder(TRANSAC_FILE, st.session_state.trans)
                st.rerun()
        
        st.divider()
        st.write(f"### Films ({len(films)})")
        for f in films:
            with st.expander(f"{f['titre']}"):
                if f.get("image_url"): st.image(f["image_url"], width=150)
                st.write(f)
                if st.button(f"Supprimer {f['titre']}", key=f"del_{f['id']}"):
                    st.session_state.films = [x for x in st.session_state.films if x['id']!=f['id']]
                    sauvegarder(FILMS_FILE, st.session_state.films)
                    st.rerun()
    elif code2 != "":
        st.error("Code faux")
