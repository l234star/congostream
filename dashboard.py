import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

GENRES_COMPLETS = ["Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", "Policier", "Romance", "Science-fiction", "Thriller", "Western"]

# INTRO VERT JAUNE ROUGE AVEC CONGOSTREAM
if "intro_done" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:999999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 4s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;top:0;left:0;">
            <div style="flex:1;background:#009543;animation: slideUp 0.7s 0.1s both;"></div>
            <div style="flex:1;background:#FBDE4A;animation: slideUp 0.7s 0.4s both;"></div>
            <div style="flex:1;background:#DC241F;animation: slideUp 0.7s 0.7s both;"></div>
        </div>
        <h1 style="z-index:10;color:white;font-size:55px;font-weight:900;letter-spacing:4px;text-align:center;animation: zoomIn 0.8s 1.2s both;text-shadow:0 0 20px black;">CONGO<span style="color:#FBDE4A;">STREAM</span></h1>
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
.stApp { background:#000; color:white; }
.netflix-title { color:#E50914; font-weight:900; font-size:38px; }
.film-card { background:#181818; border-radius:8px; overflow:hidden; border:1px solid #222; }
.film-card:hover { transform: scale(1.03); border-color:white; transition:0.3s; }
.live-dot { width:10px; height:10px; background:#E50914; border-radius:50%; display:inline-block; }
header{visibility:hidden;}
.stButton>button { background:white; color:black; font-weight:900; border-radius:6px; width:100%; }
</style>
""", unsafe_allow_html=True)

if "films" not in st.session_state:
    st.session_state.films = [
        {"id":1, "titre":"THE FIXERS", "categorie":"Série", "genre":"Action", "annee":"2026", "episodes":"10 Épisodes", "age":"16+", "desc":"Unité d'élite", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "trailer":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "image":"https://image.tmdb.org/t/p/w500/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "banner":"https://image.tmdb.org/t/p/original/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "type":"Plus", "qualite":"4K"},
        {"id":2, "titre":"Amour à Brazzaville", "categorie":"Film", "genre":"Romance", "annee":"2024", "episodes":"Film", "age":"12+", "desc":"Amour à Pointe-Noire", "youtube":"https://www.youtube.com/watch?v=jNQXAC9IVRw", "trailer":"https://www.youtube.com/watch?v=jNQXAC9IVRw", "image":"https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "banner":"https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "type":"Simple", "qualite":"HD"},
    ]
if "abonnes" not in st.session_state: st.session_state.abonnes = []
if "selected_film" not in st.session_state: st.session_state.selected_film = None
if "user_tier" not in st.session_state: st.session_state.user_tier = "Gratuit"
if "accueil" not in st.session_state:
    st.session_state.accueil = {"titre":"THE FIXERS", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k"}

c1, c2, c3 = st.columns([2,2,1])
with c1: st.markdown('<div class="netflix-title">CONGOSTREAM <span class="live-dot"></span></div>', unsafe_allow_html=True)
with c2: search = st.text_input("", placeholder="Rechercher...", label_visibility="collapsed")
with c3: menu = st.selectbox("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed")

def get_banner(film):
    return film.get("banner") or film.get("image") or "https://via.placeholder.com/1200x600"

# VUE DETAIL COMME TA PHOTO
if st.session_state.selected_film and menu == "Accueil":
    film = next((f for f in st.session_state.films if f["id"] == st.session_state.selected_film), None)
    if film:
        if st.button("⬅️ Retour Accueil"):
            st.session_state.selected_film = None
            st.rerun()

        banner_url = get_banner(film)
        st.markdown(f"""
        <div style="position:relative;">
            <img src="{banner_url}" style="width:100%; height:65vh; object-fit:cover; border-radius:12px;">
            <div style="position:absolute; top:0; left:0; width:100%; height:65vh; background: linear-gradient(to top, #000 5%, transparent 70%); border-radius:12px;"></div>
            <div style="position:absolute; bottom:20px; left:30px;">
                <h1 style="font-size:50px; font-weight:900; margin:0; color:white;">{film['titre']}</h1>
                <p style="color:#ccc;">{film['categorie']} • {film['genre']} • {film['annee']} • {film.get('episodes','')} • {film.get('age','')}</p>
                <p style="max-width:600px;">{film.get('desc','')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎬 Bande annonce (Gratuite)")
        st.video(film.get("trailer", film.get("youtube")))
        st.caption("Gratuite - tu peux quitter quand tu veux, pas obligé de finir")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Lecture - Film complet", use_container_width=True):
                if "Simple" in st.session_state.user_tier or "Plus" in st.session_state.user_tier:
                    if film.get("qualite") == "4K" and "Plus" not in st.session_state.user_tier:
                        st.warning("🔒 4K réservé PLUS 5000F - Passe en PLUS")
                    else:
                        st.video(film.get("youtube"))
                else:
                    st.error("🔒 Abonnement requis pour le film! Bande annonce gratuite seulement")
                    st.info("Va dans S'abonner > Simple 3500F ou Plus 5000F")
        with col2:
            if st.button("Plus d'infos", use_container_width=True):
                st.info(f"{film['titre']} - {film['genre']} - {film['qualite']}")

elif menu == "Accueil":
    hero = st.session_state.films[0] if st.session_state.films else None
    if hero:
        banner_url = get_banner(hero)
        st.markdown(f"""
        <div style="position:relative; margin-bottom:20px;">
            <img src="{banner_url}" style="width:100%; height:55vh; object-fit:cover; border-radius:12px;">
            <div style="position:absolute; top:0; left:0; width:100%; height:55vh; background: linear-gradient(to top, black, transparent); border-radius:12px;"></div>
            <div style="position:absolute; bottom:30px; left:30px;">
                <h1 style="font-size:50px; font-weight:900;">{hero['titre']}</h1>
                <p>{hero['categorie']} • {hero['genre']} • {hero['annee']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    tier = st.selectbox("👤 Mon forfait:", ["Gratuit (Bande annonce seulement)", "Simple - 3500F", "Plus - 5000F"])
    st.session_state.user_tier = tier

    col_f1, col_f2 = st.columns(2)
    with col_f1: cat_f = st.selectbox("CATEGORIE", ["TOUT", "Film", "Série", "Documentaire"])
    with col_f2: genre_f = st.selectbox("GENRE", ["TOUS"] + GENRES_COMPLETS)

    films = st.session_state.films
    if cat_f!= "TOUT": films = [f for f in films if f["categorie"] == cat_f]
    if genre_f!= "TOUS": films = [f for f in films if f["genre"] == genre_f]
    if search: films = [f for f in films if search.lower() in f["titre"].lower() or search.lower() in f["genre"].lower()]

    st.markdown("### Reprendre avec le profil")
    cols = st.columns(5)
    for i, film in enumerate(films):
        with cols[i % 5]:
            st.markdown('<div class="film-card">', unsafe_allow_html=True)
            st.image(film.get("image"), use_container_width=True)
            st.caption(f"{film['titre']}")
            if st.button("Voir", key=f"voir_{film['id']}", use_container_width=True):
                st.session_state.selected_film = film["id"]
                st.rerun()
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

    if st.button("Déconnexion"): st.session_state["admin"]=False; st.rerun()
    t1, t2 = st.tabs(["📤 Publier", "💰 Abonnés"])

    with t1:
        with st.form("pub_final", clear_on_submit=True):
            titre = st.text_input("Titre *")
            cA, cB = st.columns(2)
            with cA:
                categorie = st.selectbox("Catégorie", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre *", GENRES_COMPLETS)
            with cB:
                annee = st.text_input("Année", "2026")
                qualite = st.selectbox("Qualité", ["HD - Simple", "4K - Plus"])
            desc = st.text_area("Description")
            trailer = st.text_input("Lien Bande Annonce * (Gratuit)")
            film_link = st.text_input("Lien Film Complet (Payant)")
            image = st.text_input("Lien Pochette verticale")
            banner = st.text_input("Lien Bannière horizontale (pour page comme ta photo)")

            if st.form_submit_button("🔓 ENTRÉE - PUBLIER", use_container_width=True):
                if titre and trailer:
                    st.session_state.films.append({
                        "id": random.randint(100,99999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee,
                        "episodes":"Film" if categorie=="Film" else "Série", "age":"16+", "desc":desc,
                        "youtube":film_link or trailer, "trailer":trailer, "image":image or "https://via.placeholder.com/300x450",
                        "banner":banner or image, "type":qualite, "qualite":"4K" if "4K" in qualite else "HD"
                    })
                    st.success("Publié!"); st.balloons()
                else: st.warning("Titre + Bande annonce obligatoire")

    with t2:
        st.write(st.session_state.abonnes)

else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.info("**SIMPLE 3500F**\n✅ HD\n❌ Pas 4K")
    with c2: st.success("**PLUS 5000F**\n✅ 4K\n✅ Demande\n✅ Réservation 24h\n✅ Assistance 24h/24")
    with st.form("ab_final"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c})
            st.success(f"{nom} actif jusqu'au {fin}")
