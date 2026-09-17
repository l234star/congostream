import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

# --- LISTE COMPLETE DES GENRES QUE TU AS DEMANDÉ ---
GENRES_COMPLETS = [
    "Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", 
    "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", 
    "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", 
    "Policier", "Romance", "Science-fiction", "Thriller", "Western"
]

# INTRO
if "intro_done" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:99999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 3.5s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;">
            <div style="flex:1;background:#009543;animation: slideUp 0.7s 0.1s both;"></div>
            <div style="flex:1;background:#FBDE4A;animation: slideUp 0.7s 0.4s both;"></div>
            <div style="flex:1;background:#DC241F;animation: slideUp 0.7s 0.7s both;"></div>
        </div>
        <h1 style="z-index:2;color:white;font-size:60px;font-weight:900;letter-spacing:5px;animation: zoomIn 0.8s 1.2s both;">CONGO<span style="color:#FBDE4A;">STREAM</span></h1>
    </div>
    <style>
    @keyframes slideUp { from {transform: translateY(100%);} to {transform: translateY(0%);} }
    @keyframes zoomIn { from {opacity:0;transform:scale(0.5);} to {opacity:1;transform:scale(1);} }
    @keyframes fadeOut { to {opacity:0;visibility:hidden;} }
    </style>
    """, unsafe_allow_html=True)
    st.session_state.intro_done = True

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top, #1a0a00 0%, #000 70%); color:white; }
.netflix-title { color:#E50914; font-weight:900; font-size:38px; }
.film-card { background: rgba(20,20,20,0.95); border-radius:12px; padding:10px; border:1px solid #333; }
.film-card:hover { border-color:#E50914; transform: translateY(-5px); transition:0.3s; }
.badge-4k { background: gold; color:black; padding:2px 6px; border-radius:4px; font-weight:900; font-size:12px; }
.live-dot { width:10px; height:10px; background:#E50914; border-radius:50%; display:inline-block; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(229,9,20,0.7);} 70%{box-shadow:0 0 0 10px rgba(229,9,20,0);} 100%{box-shadow:0 0 0 0 rgba(229,9,20,0);} }
header{visibility:hidden;}
.stButton>button { background:#E50914; color:white; font-weight:bold; border-radius:6px; width:100%; }
</style>
""", unsafe_allow_html=True)

if "films" not in st.session_state:
    st.session_state.films = [
        {"id":1, "titre":"Boruto Naruto Next", "categorie":"Série", "genre":"Animation", "annee":"2024", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "trailer":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "image":"https://image.tmdb.org/t/p/w500/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "type":"Plus - 5000F", "qualite":"4K"},
    ]
if "accueil" not in st.session_state:
    st.session_state.accueil = {"titre":"Exclu Congo", "desc":"Netflix du Congo", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k"}
if "abonnes" not in st.session_state: st.session_state.abonnes = []
if "user_tier" not in st.session_state: st.session_state.user_tier = "Gratuit"

c1, c2, c3 = st.columns([2,2,1])
with c1: st.markdown('<div class="netflix-title">CONGOSTREAM <span class="live-dot"></span></div>', unsafe_allow_html=True)
with c2: search = st.text_input("", placeholder="Rechercher un genre, ex: Action, Thriller...", label_visibility="collapsed")
with c3: menu = st.selectbox("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed")

if menu == "Accueil":
    a = st.session_state.accueil
    st.video(a["youtube"])
    tier = st.selectbox("👤 Mon forfait:", ["Gratuit", "Simple - 3500F", "Plus - 5000F"])
    if "Plus" in tier: st.session_state.user_tier = "Plus"
    elif "Simple" in tier: st.session_state.user_tier = "Simple"
    else: st.session_state.user_tier = "Gratuit"

    if st.session_state.user_tier == "Plus":
        st.markdown('<div style="background:linear-gradient(90deg, gold, #E50914);padding:12px;border-radius:10px;color:black;font-weight:bold;">👑 PLUS - 4K | Film à la demande | Réservation 24h | Assistance 24h/24</div>', unsafe_allow_html=True)
    else:
        st.info("Passe en PLUS 5000F pour 4K + Film à la demande + Réservation 24h")

    st.divider()
    col_f1, col_f2 = st.columns(2)
    with col_f1: cat_f = st.selectbox("📁 CATEGORIE", ["TOUT", "Film", "Série", "Documentaire"])
    with col_f2: genre_f = st.selectbox("🎭 GENRE", ["TOUS"] + GENRES_COMPLETS)

    films = st.session_state.films
    if cat_f != "TOUT": films = [f for f in films if f["categorie"] == cat_f]
    if genre_f != "TOUS": films = [f for f in films if f["genre"] == genre_f]
    if search: films = [f for f in films if search.lower() in f["titre"].lower() or search.lower() in f["genre"].lower()]

    cols = st.columns(4)
    for i, film in enumerate(films):
        is_4k = film.get("qualite") == "4K"
        can_watch = not (is_4k and st.session_state.user_tier != "Plus")
        with cols[i % 4]:
            st.markdown('<div class="film-card">', unsafe_allow_html=True)
            st.image(film["image"], use_container_width=True)
            st.markdown(f"**{film['titre']}**")
            st.caption(f"{film['genre']} | {film['categorie']} | {film.get('qualite','HD')}")
            if not can_watch: st.warning("🔒 4K - PLUS uniquement")
            else:
                if st.button("Bande annonce", key=f"b_{film['id']}"): st.video(film["trailer"])
                if st.button("Regarder", key=f"r_{film['id']}"): st.video(film["youtube"])
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Espace Associé":
    st.title("Espace Associé")
    if not st.session_state.get("admin"):
        code = st.text_input("Code", type="password", placeholder="RolVie2002")
        if st.button("🔓 ENTRÉE", use_container_width=True):
            if code == "RolVie2002":
                st.session_state["admin"] = True
                st.rerun()
            else: st.error("Mauvais code")
        st.stop()

    st.success("Bienvenue Patron - Accès Directeur")
    if st.button("Déconnexion"): st.session_state["admin"]=False; st.rerun()

    t1, t2, t3, t4 = st.tabs(["📤 Publier", "🎬 Gérer", "🏠 Accueil", "💰 Abonnements"])

    with t1:
        with st.form("pub_v9", clear_on_submit=True):
            titre = st.text_input("Titre *")
            cA, cB = st.columns(2)
            with cA:
                categorie = st.selectbox("Catégorie", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre *", GENRES_COMPLETS)
            with cB:
                annee = st.text_input("Année", "2024")
                qualite = st.selectbox("Qualité", ["HD - Pour Simple", "4K - Pour PLUS"])
                type_ac = st.selectbox("Forfait", ["Gratuit", "Simple - 3500F", "Plus - 5000F"])

            st.markdown("**Bande annonce obligatoire pour Film ET Série**")
            trailer_link = st.text_input("Lien YouTube Bande Annonce *")
            trailer_file = st.file_uploader("OU Upload Bande Annonce", type=["mp4","mov","avi","mkv"])

            film_link = st.text_input("Lien Film Complet")
            film_file = st.file_uploader("OU Upload Film Complet (illimité)", type=["mp4","mkv","mov","avi"])
            image_link = st.text_input("Lien Pochette")
            image_file = st.file_uploader("OU Upload Pochette", type=["jpg","png","jpeg","webp"])

            if st.form_submit_button("🔓 ENTRÉE - PUBLIER", use_container_width=True):
                if titre and (trailer_link or trailer_file):
                    final_q = "4K" if "4K" in qualite else "HD"
                    final_img = image_link if image_link else "https://via.placeholder.com/500x750/000000/E50914?text=CONGOSTREAM"
                    st.session_state.films.append({"id": random.randint(100,9999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee, "youtube":film_link or "upload", "trailer":trailer_link or "upload", "image":final_img, "type":type_ac, "qualite":final_q})
                    st.success(f"{titre} publié en {genre} !"); st.balloons()
                else: st.warning("Titre + Bande annonce obligatoire")

    with t2:
        for film in st.session_state.films:
            with st.expander(f"{film['titre']} - {film['genre']}"):
                st.image(film["image"], width=120)
                if st.button("Supprimer", key=f"del_{film['id']}"):
                    st.session_state.films = [f for f in st.session_state.films if f["id"]!= film["id"]]; st.rerun()

    with t3:
        acc = st.session_state.accueil
        acc["titre"] = st.text_input("Titre Accueil", acc["titre"])
        acc["youtube"] = st.text_input("Youtube Accueil", acc["youtube"])
        if st.button("🔓 ENTRÉE - Sauver Accueil"): st.success("Sauvé")

    with t4:
        st.write(st.session_state.abonnes)

else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: st.info("**SIMPLE 3500F**\n\n✅ HD\n\n❌ Pas de 4K")
    with col2: st.success("**PLUS 5000F**\n\n✅ 4K\n✅ Film à la demande\n✅ Réservation 24h\n✅ Assistance 24h/24")
    with st.form("ab_v9"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c, "statut":"Actif"})
            st.success(f"Actif jusqu'au {fin}"); st.balloons()
