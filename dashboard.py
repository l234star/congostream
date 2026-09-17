import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

GENRES_COMPLETS = ["Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", "Policier", "Romance", "Science-fiction", "Thriller", "Western"]

st.markdown("""
<style>
.stApp { background:#000; color:white; }
.netflix-title { color:#E50914; font-weight:900; font-size:38px; }
.netflix-hero { position:relative; height:75vh; border-radius:15px; overflow:hidden; background: linear-gradient(to top, #000 0%, transparent 50%), linear-gradient(to right, #000 30%, transparent 80%); }
.hero-content { position:absolute; bottom:30px; left:40px; z-index:2; max-width:600px; }
.film-card { background:#181818; border-radius:8px; overflow:hidden; cursor:pointer; transition:0.3s; border:1px solid #222; }
.film-card:hover { transform: scale(1.05); border-color:white; }
.live-dot { width:10px; height:10px; background:#E50914; border-radius:50%; display:inline-block; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(229,9,20,0.7);} 70%{box-shadow:0 0 0 10px rgba(229,9,20,0);} 100%{box-shadow:0 0 0 0 rgba(229,9,20,0);} }
header{visibility:hidden;}
.stButton>button { background:white; color:black; font-weight:900; border-radius:6px; }
.btn-red button { background:#E50914!important; color:white!important; }
</style>
""", unsafe_allow_html=True)

if "films" not in st.session_state:
    st.session_state.films = [
        {"id":1, "titre":"THE FIXERS", "categorie":"Série", "genre":"Action", "annee":"2026", "episodes":"10 Épisodes", "age":"16+", "desc":"Unité d'élite qui fixe les problèmes que personne ne peut résoudre. Action non-stop.", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "trailer":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "image":"https://image.tmdb.org/t/p/w500/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "banner":"https://image.tmdb.org/t/p/original/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "type":"Plus", "qualite":"4K"},
        {"id":2, "titre":"Amour à Brazzaville", "categorie":"Film", "genre":"Romance", "annee":"2024", "episodes":"Film", "age":"12+", "desc":"Histoire d'amour entre deux jeunes de Pointe-Noire.", "youtube":"https://www.youtube.com/watch?v=jNQXAC9IVRw", "trailer":"https://www.youtube.com/watch?v=jNQXAC9IVRw", "image":"https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "banner":"https://image.tmdb.org/t/p/original/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "type":"Simple", "qualite":"HD"},
    ]
if "abonnes" not in st.session_state: st.session_state.abonnes = []
if "selected_film" not in st.session_state: st.session_state.selected_film = None
if "user_tier" not in st.session_state: st.session_state.user_tier = "Gratuit"
if "accueil" not in st.session_state:
    st.session_state.accueil = {"titre":"THE FIXERS", "desc":"Série Action 2026", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k"}

# HEADER
c1, c2, c3 = st.columns([2,2,1])
with c1: st.markdown('<div class="netflix-title">CONGOSTREAM <span class="live-dot"></span></div>', unsafe_allow_html=True)
with c2: search = st.text_input("", placeholder="🔍 Films, séries, genres...", label_visibility="collapsed")
with c3: menu = st.selectbox("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed")

# ================= VUE DETAIL FILM COMME SUR TA PHOTO =================
if st.session_state.selected_film and menu == "Accueil":
    film = next((f for f in st.session_state.films if f["id"] == st.session_state.selected_film), None)
    if film:
        if st.button("⬅️ Retour"):
            st.session_state.selected_film = None
            st.rerun()

        # HERO COMME NETFLIX
        st.markdown(f"""
        <div style="position:relative;">
            <img src="{film['banner']}" style="width:100%; height:70vh; object-fit:cover; border-radius:10px; opacity:0.6;">
            <div style="position:absolute; bottom:0; left:0; width:100%; height:70vh; background: linear-gradient(to top, black 10%, transparent 80%);"></div>
            <div style="position:absolute; bottom:30px; left:40px;">
                <h1 style="font-size:60px; font-weight:900; margin:0;">{film['titre']}</h1>
                <p style="font-size:18px; color:#ccc;">{film['categorie']} • {film['genre']} • {film['annee']} • {film['episodes']} • {film['age']}</p>
                <p style="max-width:600px; font-size:16px;">{film['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # BANDE ANNONCE GRATUITE - SE LANCE DIRECT
        st.markdown("### 🎬 Bande annonce (Gratuite - tu peux quitter à tout moment)")
        st.video(film["trailer"])
        st.caption("La bande annonce est gratuite. Le film complet nécessite un abonnement.")

        # BOUTONS LECTURE
        col1, col2, col3 = st.columns([1,1,3])
        with col1:
            if st.button("▶️ Lecture", key="lecture_film", use_container_width=True):
                if st.session_state.user_tier in ["Simple - 3500F", "Plus - 5000F", "Simple", "Plus"]:
                    st.markdown("### 🎬 Film Complet")
                    st.video(film["youtube"])
                    if film.get("qualite") == "4K" and "Plus" not in str(st.session_state.user_tier):
                        st.warning("Ce film est en 4K, passe en PLUS 5000F pour la qualité max")
                else:
                    st.error("🔒 Abonnement requis pour regarder le film! Bande annonce gratuite seulement.")
                    st.warning("Va dans S'abonner pour prendre Simple 3500F ou Plus 5000F")
        with col2:
            if st.button("Plus d'infos", key="infos"):
                st.info(f"**{film['titre']}**\n\nGenre: {film['genre']}\nAnnée: {film['annee']}\nQualité: {film['qualite']}\nType: {film['categorie']}\n\n{film['desc']}")

        st.divider()
        st.markdown("#### Reprendre avec le profil")
        cols = st.columns(6)
        for i, f in enumerate(st.session_state.films[:6]):
            with cols[i % 6]:
                if st.button(f"{f['titre']}", key=f"rel_{f['id']}"):
                    st.session_state.selected_film = f["id"]
                    st.rerun()
                st.image(f["image"], use_container_width=True)

# ================= ACCUEIL NORMAL =================
elif menu == "Accueil":
    # HERO PRINCIPAL
    hero = st.session_state.films[0] if st.session_state.films else None
    if hero:
        st.markdown(f"""
        <div style="position:relative; margin-bottom:20px;">
            <img src="{hero['banner']}" style="width:100%; height:60vh; object-fit:cover; border-radius:10px; opacity:0.7;">
            <div style="position:absolute; bottom:0; left:0; width:100%; height:60vh; background: linear-gradient(to top, black, transparent);"></div>
            <div style="position:absolute; bottom:40px; left:40px;">
                <h1 style="font-size:55px; font-weight:900;">{hero['titre']}</h1>
                <p>{hero['categorie']} • {hero['genre']} • {hero['annee']} • {hero['episodes']} • {hero['age']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    tier = st.selectbox("👤 Mon abonnement:", ["Gratuit (Bande annonce seulement)", "Simple - 3500F", "Plus - 5000F"], key="tier_main")
    st.session_state.user_tier = tier

    col_f1, col_f2 = st.columns(2)
    with col_f1: cat_f = st.selectbox("📁 CATEGORIE", ["TOUT", "Film", "Série", "Documentaire"])
    with col_f2: genre_f = st.selectbox("🎭 GENRE", ["TOUS"] + GENRES_COMPLETS)

    films = st.session_state.films
    if cat_f!= "TOUT": films = [f for f in films if f["categorie"] == cat_f]
    if genre_f!= "TOUS": films = [f for f in films if f["genre"] == genre_f]
    if search: films = [f for f in films if search.lower() in f["titre"].lower() or search.lower() in f["genre"].lower()]

    st.markdown(f"### Reprendre avec le profil de {tier.split()[0]}")
    cols = st.columns(5)
    for i, film in enumerate(films):
        with cols[i % 5]:
            st.markdown('<div class="film-card">', unsafe_allow_html=True)
            st.image(film["image"], use_container_width=True)
            st.caption(f"{film['titre']} • {film['genre']}")
            # CLIC = OUVRE LA PAGE COMME SUR TA PHOTO
            if st.button("Voir", key=f"voir_{film['id']}", use_container_width=True):
                st.session_state.selected_film = film["id"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ================= ESPACE ASSOCIE =================
elif menu == "Espace Associé":
    st.title("Espace Associé - BOSS / Directeur Seph")
    if not st.session_state.get("admin"):
        code = st.text_input("Code", type="password", placeholder="RolVie2002")
        if st.button("🔓 ENTRÉE", use_container_width=True):
            if code == "RolVie2002":
                st.session_state["admin"] = True
                st.rerun()
            else: st.error("Mauvais code")
        st.stop()

    if st.button("Déconnexion"): st.session_state["admin"]=False; st.session_state.selected_film=None; st.rerun()

    t1, t2, t3 = st.tabs(["📤 Publier", "🎬 Gérer", "💰 Abonnements Simple/Plus"])

    with t1:
        with st.form("pub_netflix", clear_on_submit=True):
            titre = st.text_input("Titre * ex: THE FIXERS")
            cA, cB = st.columns(2)
            with cA:
                categorie = st.selectbox("Catégorie", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre *", GENRES_COMPLETS)
                annee = st.text_input("Année", "2026")
                episodes = st.text_input("Episodes / Durée", "10 Épisodes")
            with cB:
                age = st.selectbox("Age", ["Tout public", "7+", "12+", "16+", "18+"])
                qualite = st.selectbox("Qualité", ["HD - Simple", "4K - Plus"])
                type_ac = st.selectbox("Forfait requis", ["Simple - 3500F", "Plus - 5000F"])

            desc = st.text_area("Description courte *")
            trailer = st.text_input("Lien Bande Annonce YouTube * (Gratuit)")
            film_link = st.text_input("Lien Film Complet YouTube (Payant - bloqué sans abo)")
            image = st.text_input("Lien Pochette (vertical)")
            banner = st.text_input("Lien Bannière large (horizontal) pour page détail")

            trailer_up = st.file_uploader("OU Upload Bande Annonce (illimité)", type=["mp4","mov","mkv"])
            film_up = st.file_uploader("OU Upload Film (illimité)", type=["mp4","mkv","mov","avi"])

            if st.form_submit_button("🔓 ENTRÉE - PUBLIER", use_container_width=True):
                if titre and trailer:
                    st.session_state.films.append({
                        "id": random.randint(100,99999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee,
                        "episodes":episodes, "age":age, "desc":desc, "youtube":film_link or "upload_film",
                        "trailer":trailer or "upload_trailer", "image":image or "https://via.placeholder.com/300x450",
                        "banner":banner or image, "type":type_ac, "qualite":"4K" if "4K" in qualite else "HD"
                    })
                    st.success("Publié! Comme sur ta photo Netflix"); st.balloons()
                else: st.warning("Titre + Bande annonce obligatoire")

    with t2:
        for f in st.session_state.films:
            with st.expander(f"{f['titre']}"):
                if st.button("Supprimer", key=f"del_{f['id']}"):
                    st.session_state.films = [x for x in st.session_state.films if x["id"]!= f["id"]]; st.rerun()

    with t3:
        for ab in st.session_state.abonnes:
            st.write(f"{ab['nom']} - {ab['type']} - {ab['fin']}")

else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.info("**SIMPLE 3500F**\n\n✅ Films/Séries HD\n✅ Bande annonce gratuite\n❌ Pas de 4K")
    with c2: st.success("**PLUS 5000F**\n\n✅ Tout + 4K\n✅ Film à la demande\n✅ Réservation 24h\n✅ Assistance 24h/24")
    with st.form("ab_netflix"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c, "statut":"Actif"})
            st.success(f"{nom} - {type_c} actif jusqu'au {fin}. Maintenant tu peux cliquer Lecture sur les films!")
