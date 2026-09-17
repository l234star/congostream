import streamlit as st

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

# --- CSS NETFLIX PRO ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: white; }
    h1, h2, h3 { color: white; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .netflix-red { color: #E50914; font-weight: 900; letter-spacing: 2px; }
    .film-card {
        background: #181818; border-radius: 8px; padding: 10px; 
        transition: transform 0.3s; border: 1px solid #333;
    }
    .film-card:hover { transform: scale(1.05); border-color: #E50914; }
    .genre-badge { background: #E50914; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .stButton>button { background-color: #E50914; color: white; border: none; font-weight: bold; border-radius: 4px; }
    .stButton>button:hover { background-color: #b81d24; color: white; }
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
if "films" not in st.session_state:
    st.session_state.films = [
        {"titre": "Boruto: Naruto Next", "categorie": "Série", "genre": "ANIMÉ", "annee": "2024", "youtube": "https://www.youtube.com/watch?v=Qp3b-Rhse9k", "image": "https://image.tmdb.org/t/p/w500/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "type": "Premium"},
        {"titre": "Lupin - Braquage à Pointe-Noire", "categorie": "Film", "genre": "SUSPENSE", "annee": "2023", "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "image": "https://image.tmdb.org/t/p/w500/aAgGrfBwna1F90K7lhfoE2D4zq0.jpg", "type": "Premium"},
        {"titre": "Amour à Brazzaville", "categorie": "Film", "genre": "ROMANTIQUE", "annee": "2024", "youtube": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "image": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "type": "Gratuit"},
        {"titre": "Histoire du Congo", "categorie": "Documentaire", "genre": "GUERRE", "annee": "2022", "youtube": "https://www.youtube.com/watch?v=9bZkp7q19f0", "image": "https://image.tmdb.org/t/p/w500/7RyHsO4yDXtBv1zUU3mTpHeQd.jpg", "type": "Gratuit"},
        {"titre": "Les Aventures de Kito", "categorie": "Série", "genre": "JEUNESSE", "annee": "2024", "youtube": "https://www.youtube.com/watch?v=kJQP7kiw5Fk", "image": "https://image.tmdb.org/t/p/w500/qW4crfED8mpNDadSmMdi7ZDzhXF.jpg", "type": "Gratuit"},
    ]

# --- HEADER NETFLIX ---
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown('<h1 class="netflix-red">CONGOSTREAM</h1>', unsafe_allow_html=True)
with col2:
    search = st.text_input("", placeholder="🔍 Rechercher un film, série, animé...", label_visibility="collapsed")

# --- FILTRES CATÉGORIES ET GENRES ---
st.markdown("###")
c1, c2, c3 = st.columns([2,2,3])
with c1:
    cat_filtre = st.selectbox("📁 CATÉGORIE", ["TOUT", "Film", "Série", "Documentaire"])
with c2:
    genre_filtre = st.selectbox("🎭 GENRE", ["TOUS", "ANIMÉ", "SUSPENSE", "ROMANTIQUE", "GUERRE", "JEUNESSE", "ACTION", "COMÉDIE"])
with c3:
    menu = st.selectbox("MENU", ["Accueil", "Espace Associé - Seph", "S'abonner 3500F / 2 Mois"])

# --- LOGIQUE AFFICHAGE ---
if menu == "Accueil" or menu.startswith("Accueil"):
    # Filtrage
    films_filtres = st.session_state.films
    if cat_filtre != "TOUT":
        films_filtres = [f for f in films_filtres if f["categorie"] == cat_filtre]
    if genre_filtre != "TOUS":
        films_filtres = [f for f in films_filtres if f["genre"] == genre_filtre]
    if search:
        films_filtres = [f for f in films_filtres if search.lower() in f["titre"].lower()]

    # Hero
    if not search and cat_filtre=="TOUT" and genre_filtre=="TOUS":
        st.video("https://www.youtube.com/watch?v=Qp3b-Rhse9k")
        st.markdown("## 🔥 TENDANCE N°1 AU CONGO AUJOURD'HUI")

    st.markdown(f"### {genre_filtre if genre_filtre!='TOUS' else cat_filtre if cat_filtre!='TOUT' else 'Pour Vous'}")
    
    cols = st.columns(4)
    for i, film in enumerate(films_filtres):
        with cols[i % 4]:
            st.markdown(f'<div class="film-card">', unsafe_allow_html=True)
            st.image(film["image"], use_container_width=True)
            st.markdown(f'<span class="genre-badge">{film["genre"]}</span> <small>{film["annee"]} • {film["categorie"]}</small>', unsafe_allow_html=True)
            st.markdown(f'**{film["titre"]}**')
            if film["type"] == "Premium":
                st.caption("🔒 Premium - 3500F")
            else:
                st.caption("🟢 Gratuit")
            
            if st.button(f"▶️ Regarder", key=f"watch_{i}"):
                st.session_state[f"play_{i}"] = True
            
            if st.session_state.get(f"play_{i}"):
                st.video(film["youtube"])
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")

elif "Espace Associé" in menu:
    st.title("Espace Associé")
    code = st.text_input("Mot de passe Seph :", type="password")
    if st.button("🔓 ENTRÉE", use_container_width=True):
        if code == "RolVie2002":
            st.session_state["admin"] = True
        else:
            st.error("Code incorrect")

    if st.session_state.get("admin"):
        st.success("👋 Bienvenue Monsieur Seph NTOUMOU - Patron de CONGOSTREAM")
        st.markdown("---")
        with st.form("publish_pro", clear_on_submit=True):
            st.subheader("📤 Publier du contenu PRO")
            colA, colB = st.columns(2)
            with colA:
                titre = st.text_input("Titre du film/série *")
                categorie = st.selectbox("Catégorie *", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre *", ["ANIMÉ", "SUSPENSE", "ROMANTIQUE", "GUERRE", "JEUNESSE", "ACTION", "COMÉDIE", "DRAME"])
            with colB:
                annee = st.text_input("Année", value="2024")
                youtube = st.text_input("Lien YouTube *")
                image = st.text_input("Lien image affiche (optionnel)")
                type_acc = st.selectbox("Accès", ["Gratuit", "Premium - 3500F"])
            
            publier = st.form_submit_button("🚀 PUBLIER SUR CONGOSTREAM", use_container_width=True)
            if publier:
                if titre and youtube:
                    if not image:
                        image = "https://via.placeholder.com/500x750/181818/E50914?text=CONGOSTREAM"
                    st.session_state.films.append({
                        "titre": titre, "categorie": categorie, "genre": genre, 
                        "annee": annee, "youtube": youtube, "image": image, "type": type_acc
                    })
                    st.success(f"✅ {titre} ajouté en {categorie} > {genre} !")
                    st.balloons()
                else:
                    st.warning("Titre et Lien YouTube obligatoires !")

else: # Abonnement
    st.markdown('<h1 class="netflix-red">3500F / 2 MOIS</h1>', unsafe_allow_html=True)
    st.markdown("### Débloque tout le catalogue Premium 🇨🇬")
    st.info("1️⃣ Envoie 3500F par MTN MoMo au **066778924**\n\n2️⃣ Entre l'ID de transaction")
    id_mtn = st.text_input("ID MTN")
    if st.button("Activer mon accès Premium"):
        st.success("Reçu ! Accès Premium activé sous 10 min. Merci !")
