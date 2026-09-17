import streamlit as st
from datetime import datetime, timedelta, date
import random, os

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

GENRES_COMPLETS = ["Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", "Policier", "Romance", "Science-fiction", "Thriller", "Western"]

# INTRO V14 - CONGOSTREAM TOUT COURT
if "intro_done_v14" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:9999999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 3.8s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;top:0;left:0;">
            <div style="flex:1;background:#009543;"></div>
            <div style="flex:1;background:#FBDE4A;"></div>
            <div style="flex:1;background:#DC241F;"></div>
        </div>
        <h1 style="z-index:10;color:white;font-size:58px;font-weight:900;letter-spacing:6px;text-align:center;">CONGOSTREAM</h1>
    </div>
    <style>
    @keyframes fadeOut { to {opacity:0;visibility:hidden;} }
    </style>
    """, unsafe_allow_html=True)
    st.session_state.intro_done_v14 = True

st.markdown("""
<style>
.stApp { background:#000; color:white; }
.netflix-title { color:#E50914; font-weight:900; font-size:38px; }
.film-card { background:#181818; border-radius:8px; overflow:hidden; border:1px solid #222; padding:8px; }
.btn-delete button { background:#DC241F!important; color:white!important; }
header{visibility:hidden;}
.stButton>button { background:white; color:black; font-weight:900; border-radius:6px; width:100%; }
</style>
""", unsafe_allow_html=True)

os.makedirs("videos", exist_ok=True)
os.makedirs("trailers", exist_ok=True)
os.makedirs("images", exist_ok=True)

if "films" not in st.session_state: st.session_state.films = []
if "abonnes" not in st.session_state: st.session_state.abonnes = []
if "selected_film" not in st.session_state: st.session_state.selected_film = None
if "user_tier" not in st.session_state: st.session_state.user_tier = "Gratuit"

c1, c2, c3 = st.columns([2,2,1])
with c1: st.markdown('<div class="netflix-title">CONGOSTREAM</div>', unsafe_allow_html=True)
with c2: search = st.text_input("", placeholder="Rechercher...", label_visibility="collapsed")
with c3: menu = st.selectbox("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed")

def save_file(f, folder):
    if f:
        p = os.path.join(folder, f.name)
        with open(p, "wb") as out: out.write(f.getbuffer())
        return p
    return None

if st.session_state.selected_film and menu == "Accueil":
    film = next((f for f in st.session_state.films if f["id"] == st.session_state.selected_film), None)
    if film:
        if st.button("⬅️ Retour"): st.session_state.selected_film=None; st.rerun()
        if film.get("image_path") and os.path.exists(film["image_path"]): st.image(film["image_path"], use_container_width=True)
        st.title(film['titre'])
        if film.get("is_annonce") and film.get("date_sortie"):
            jours = (film["date_sortie"] - date.today()).days
            st.warning(f"🔔 ANNONCE - Sortie le {film['date_sortie'].strftime('%d/%m/%Y')} - J-{jours}" if jours>0 else "Sortie aujourd'hui!")
        st.markdown("### 🎬 Bande annonce (Gratuite)")
        if film.get("trailer_path") and os.path.exists(film["trailer_path"]): st.video(film["trailer_path"])
        if not film.get("is_annonce"):
            if st.button("▶️ Lecture Film Complet", use_container_width=True):
                if "Simple" in st.session_state.user_tier or "Plus" in st.session_state.user_tier:
                    if film.get("film_path") and os.path.exists(film["film_path"]): st.video(film["film_path"])
                    else: st.error("Film complet pas dispo")
                else: st.error("🔒 Abonnement requis!")

elif menu == "Accueil":
    tier = st.selectbox("👤 Mon forfait:", ["Gratuit (Bande annonce seulement)", "Simple - 3500F", "Plus - 5000F"])
    st.session_state.user_tier = tier
    films = st.session_state.films
    if search: films = [f for f in films if search.lower() in f["titre"].lower()]
    annonces = [f for f in films if f.get("is_annonce")]
    if annonces:
        st.markdown("## 🔔 Annonces - Prochaines Sorties")
        cols = st.columns(4)
        for i, film in enumerate(annonces):
            with cols[i % 4]:
                if film.get("image_path") and os.path.exists(film["image_path"]): st.image(film["image_path"], use_container_width=True)
                st.write(f"**{film['titre']}**")
                if film.get("date_sortie"): st.caption(f"Sortie: {film['date_sortie']}")
                if st.button("Voir annonce", key=f"ann_{film['id']}"): st.session_state.selected_film=film["id"]; st.rerun()
    dispo = [f for f in films if not f.get("is_annonce")]
    st.markdown("## 🎬 Films Disponibles")
    cols = st.columns(4)
    for i, film in enumerate(dispo):
        with cols[i % 4]:
            st.markdown('<div class="film-card">', unsafe_allow_html=True)
            if film.get("image_path") and os.path.exists(film["image_path"]): st.image(film["image_path"], use_container_width=True)
            else: st.image("https://via.placeholder.com/300x450", use_container_width=True)
            st.write(f"**{film['titre']}** - {film['genre']}")
            if st.button("Voir", key=f"voir_{film['id']}"): st.session_state.selected_film=film["id"]; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Espace Associé":
    st.title("Espace Associé - BOSS")
    if not st.session_state.get("admin"):
        code = st.text_input("Code", type="password", placeholder="RolVie2002")
        if st.button("🔓 ENTRÉE", use_container_width=True):
            if code == "RolVie2002": st.session_state["admin"]=True; st.rerun()
            else: st.error("Mauvais code")
        st.stop()
    if st.button("Déconnexion"): st.session_state["admin"]=False; st.rerun()
    t1, t2 = st.tabs(["📤 Publier", "🗑️ Gérer / Supprimer"])
    with t1:
        with st.form("pub_final_v14", clear_on_submit=True):
            titre = st.text_input("Titre *")
            is_annonce = st.checkbox("🔔 Bande annonce d'annonce (avec date)")
            cA, cB = st.columns(2)
            with cA:
                categorie = st.selectbox("Catégorie", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre *", GENRES_COMPLETS)
            with cB:
                annee = st.text_input("Année", "2026")
                qualite = st.selectbox("Qualité", ["HD - Simple", "4K - Plus"])
                date_sortie = st.date_input("📅 Date de sortie", value=date.today()+timedelta(days=7)) if is_annonce else None
            desc = st.text_area("Description")
            trailer_file = st.file_uploader("Upload Bande Annonce *", type=["mp4","mov","mkv","avi"])
            film_file = st.file_uploader("Upload Film Complet (si pas annonce)", type=["mp4","mkv","mov","avi"]) if not is_annonce else None
            image_file = st.file_uploader("Upload Affiche", type=["jpg","png","jpeg","webp"])
            if st.form_submit_button("🔓 ENTRÉE - PUBLIER", use_container_width=True):
                if titre and trailer_file:
                    tp = save_file(trailer_file, "trailers")
                    fp = save_file(film_file, "videos") if film_file else None
                    ip = save_file(image_file, "images") if image_file else None
                    st.session_state.films.append({"id": random.randint(100,99999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee, "desc":desc, "trailer_path":tp, "film_path":fp, "image_path":ip, "qualite":"4K" if "4K" in qualite else "HD", "is_annonce":is_annonce, "date_sortie":date_sortie})
                    st.success("Publié!"); st.balloons()
                else: st.warning("Titre + Bande annonce obligatoire")
    with t2:
        for film in st.session_state.films[:]:
            col1, col2, col3 = st.columns([1,3,1])
            with col2: st.write(f"**{film['titre']}** - {film['genre']} {'🔔 ANNONCE' if film.get('is_annonce') else ''}")
            with col3:
                if st.button("🗑️ Supprimer", key=f"del_{film['id']}"):
                    for p in [film.get("trailer_path"), film.get("film_path"), film.get("image_path")]:
                        if p and os.path.exists(p):
                            try: os.remove(p)
                            except: pass
                    st.session_state.films = [f for f in st.session_state.films if f["id"] != film["id"]]; st.rerun()
else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    with st.form("ab_v14"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c})
            st.success(f"{nom} actif jusqu'au {fin}")
