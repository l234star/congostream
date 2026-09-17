import streamlit as st
from datetime import datetime, timedelta, date
import random, os

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

GENRES_COMPLETS = ["Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", "Policier", "Romance", "Science-fiction", "Thriller", "Western"]

# INTRO CONGOSTREAM
if "intro_done" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:999999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 4s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;top:0;left:0;">
            <div style="flex:1;background:#009543;animation: slideUp 0.7s 0.1s both;"></div>
            <div style="flex:1;background:#FBDE4A;animation: slideUp 0.7s 0.4s both;"></div>
            <div style="flex:1;background:#DC241F;animation: slideUp 0.7s 0.7s both;"></div>
        </div>
        <h1 style="z-index:10;color:white;font-size:55px;font-weight:900;letter-spacing:4px;animation: zoomIn 0.8s 1.2s both;">CONGO<span style="color:#FBDE4A;">STREAM</span></h1>
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
.film-card { background:#181818; border-radius:8px; overflow:hidden; border:1px solid #222; padding:8px; }
.film-card:hover { border-color:white; transform:scale(1.02); transition:0.2s; }
.badge-annonce { background:#FBDE4A; color:black; padding:3px 8px; border-radius:4px; font-weight:900; font-size:11px; }
.badge-4k { background:gold; color:black; padding:2px 6px; border-radius:4px; font-weight:900; font-size:11px; }
header{visibility:hidden;}
.stButton>button { background:white; color:black; font-weight:900; border-radius:6px; width:100%; }
.btn-delete button { background:#DC241F!important; color:white!important; }
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

def save_file(uploaded_file, folder):
    if uploaded_file:
        path = os.path.join(folder, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return path
    return None

# VUE DETAIL
if st.session_state.selected_film and menu == "Accueil":
    film = next((f for f in st.session_state.films if f["id"] == st.session_state.selected_film), None)
    if film:
        if st.button("⬅️ Retour"):
            st.session_state.selected_film = None
            st.rerun()

        if film.get("image_path") and os.path.exists(film["image_path"]):
            st.image(film["image_path"], use_container_width=True)
        
        st.title(film['titre'])
        if film.get("is_annonce"):
            jours = (film.get("date_sortie") - date.today()).days if film.get("date_sortie") else 0
            if jours > 0:
                st.warning(f"🔔 ANNONCE - Sortie dans {jours} jours le {film.get('date_sortie').strftime('%d/%m/%Y')}")
            else:
                st.success(f"🔔 Sortie aujourd'hui! {film.get('date_sortie')}")
        else:
            st.caption(f"{film['categorie']} • {film['genre']} • {film['annee']} • {film.get('qualite','HD')}")

        st.markdown("### 🎬 Bande annonce (Gratuite)")
        if film.get("trailer_path") and os.path.exists(film["trailer_path"]):
            st.video(film["trailer_path"])
        else:
            st.warning("Bande annonce non disponible")

        if not film.get("is_annonce"):
            if st.button("▶️ Lecture Film Complet", use_container_width=True):
                if "Simple" in st.session_state.user_tier or "Plus" in st.session_state.user_tier:
                    if film.get("film_path") and os.path.exists(film["film_path"]):
                        st.video(film["film_path"])
                    else:
                        st.error("Film complet pas encore dispo")
                else:
                    st.error("🔒 Abonnement requis pour le film complet!")

elif menu == "Accueil":
    tier = st.selectbox("👤 Mon forfait:", ["Gratuit (Bande annonce seulement)", "Simple - 3500F", "Plus - 5000F"])
    st.session_state.user_tier = tier

    # FILTRES
    col_f1, col_f2 = st.columns(2)
    with col_f1: cat_f = st.selectbox("CATEGORIE", ["TOUT", "Film", "Série", "Documentaire"])
    with col_f2: genre_f = st.selectbox("GENRE", ["TOUS"] + GENRES_COMPLETS)

    films = st.session_state.films
    if cat_f!= "TOUT": films = [f for f in films if f["categorie"] == cat_f]
    if genre_f!= "TOUS": films = [f for f in films if f["genre"] == genre_f]
    if search: films = [f for f in films if search.lower() in f["titre"].lower()]

    # SECTION 1 : ANNONCES AVEC DATES
    annonces = [f for f in films if f.get("is_annonce")]
    if annonces:
        st.markdown("## 🔔 Annonces - Prochaines Sorties")
        cols = st.columns(4)
        for i, film in enumerate(annonces):
            with cols[i % 4]:
                st.markdown('<div class="film-card" style="border:1px solid #FBDE4A;">', unsafe_allow_html=True)
                if film.get("image_path") and os.path.exists(film["image_path"]):
                    st.image(film["image_path"], use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/300x450/111/FBDE4A?text=BIENTOT", use_container_width=True)
                st.markdown(f'<span class="badge-annonce">ANNONCE</span> **{film["titre"]}**', unsafe_allow_html=True)
                if film.get("date_sortie"):
                    st.caption(f"Sortie: {film['date_sortie'].strftime('%d/%m/%Y')}")
                    jours = (film["date_sortie"] - date.today()).days
                    if jours > 0: st.write(f"⏳ J-{jours}")
                if st.button("Voir annonce", key=f"ann_{film['id']}", use_container_width=True):
                    st.session_state.selected_film = film["id"]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # SECTION 2 : FILMS DISPONIBLES
    dispo = [f for f in films if not f.get("is_annonce")]
    st.markdown("## 🎬 Films & Séries Disponibles")
    if not dispo:
        st.info("Aucun film dispo. Publie tes vidéos dans Espace Associé.")
    else:
        cols = st.columns(4)
        for i, film in enumerate(dispo):
            with cols[i % 4]:
                st.markdown('<div class="film-card">', unsafe_allow_html=True)
                if film.get("image_path") and os.path.exists(film["image_path"]):
                    st.image(film["image_path"], use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/300x450/111/E50914?text=CONGOSTREAM", use_container_width=True)
                badge = '<span class="badge-4k">4K</span>' if film.get("qualite")=="4K" else ""
                st.markdown(f"{badge} **{film['titre']}**", unsafe_allow_html=True)
                st.caption(f"{film['genre']} | {film['qualite']}")
                if st.button("Voir", key=f"voir_{film['id']}", use_container_width=True):
                    st.session_state.selected_film = film["id"]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Espace Associé":
    st.title("Espace Associé - BOSS / Seph")
    if not st.session_state.get("admin"):
        code = st.text_input("Code", type="password", placeholder="RolVie2002")
        if st.button("🔓 ENTRÉE", use_container_width=True):
            if code == "RolVie2002":
                st.session_state["admin"] = True
                st.rerun()
            else: st.error("Mauvais code")
        st.stop()

    if st.button("Déconnexion"): st.session_state["admin"]=False; st.rerun()

    t1, t2, t3 = st.tabs(["📤 Publier", "🗑️ Gérer / Supprimer", "💰 Abonnés"])

    with t1:
        st.markdown("### 1. Publier Film Complet OU 2. Annonce Simple avec date")
        with st.form("pub_annonce", clear_on_submit=True):
            titre = st.text_input("Titre *")
            
            is_annonce = st.checkbox("🔔 C'est juste une BANDE ANNONCE D'ANNONCE pour annoncer la date (pas de film complet encore)")
            
            cA, cB = st.columns(2)
            with cA:
                categorie = st.selectbox("Catégorie", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre *", GENRES_COMPLETS)
            with cB:
                annee = st.text_input("Année", "2026")
                qualite = st.selectbox("Qualité", ["HD - Simple", "4K - Plus"])
                if is_annonce:
                    date_sortie = st.date_input("📅 Date de publication / sortie prévue", value=date.today() + timedelta(days=7))
                else:
                    date_sortie = None

            desc = st.text_area("Description / Message d'annonce")
            
            st.markdown("**Bande annonce * (obligatoire)**")
            trailer_file = st.file_uploader("Upload Bande Annonce depuis dossier", type=["mp4","mov","mkv","avi"], key="tr_annonce")
            
            if not is_annonce:
                st.markdown("**Film complet (si dispo maintenant)**")
                film_file = st.file_uploader("Upload Film Complet", type=["mp4","mkv","mov","avi"], key="film_complet")
            else:
                film_file = None
                st.info("Mode Annonce: seul la bande annonce sera visible + compte à rebours jusqu'à la date")

            image_file = st.file_uploader("Upload Pochette / Affiche", type=["jpg","png","jpeg","webp"], key="img_annonce")

            if st.form_submit_button("🔓 ENTRÉE - PUBLIER", use_container_width=True):
                if titre and trailer_file:
                    trailer_path = save_file(trailer_file, "trailers")
                    film_path = save_file(film_file, "videos") if film_file else None
                    image_path = save_file(image_file, "images") if image_file else None

                    st.session_state.films.append({
                        "id": random.randint(100,99999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee,
                        "desc":desc, "trailer_path":trailer_path, "film_path":film_path, "image_path":image_path,
                        "qualite":"4K" if "4K" in qualite else "HD", "is_annonce":is_annonce, "date_sortie":date_sortie
                    })
                    if is_annonce:
                        st.success(f"🔔 Annonce '{titre}' publiée! Sortie prévue le {date_sortie}")
                    else:
                        st.success(f"✅ {titre} publié!")
                    st.balloons()
                else:
                    st.warning("Titre + Bande annonce obligatoire")

    with t2:
        st.markdown("### 🗑️ Supprimer facilement les vieux films / annonces")
        if not st.session_state.films:
            st.info("Aucun film")
        else:
            for film in st.session_state.films[:]:
                col1, col2, col3 = st.columns([1,3,1])
                with col1:
                    if film.get("image_path") and os.path.exists(film["image_path"]):
                        st.image(film["image_path"], width=80)
                with col2:
                    type_badge = "🔔 ANNONCE" if film.get("is_annonce") else "🎬 FILM"
                    date_info = f" - Sortie {film['date_sortie']}" if film.get("date_sortie") else ""
                    st.write(f"**{type_badge} - {film['titre']}** ({film['genre']}){date_info}")
                    st.caption(f"{film.get('desc','')[:60]}...")
                with col3:
                    st.markdown('<div class="btn-delete">', unsafe_allow_html=True)
                    if st.button("🗑️ Supprimer", key=f"del_{film['id']}", use_container_width=True):
                        # Supprime fichiers physiques aussi
                        for p in [film.get("trailer_path"), film.get("film_path"), film.get("image_path")]:
                            if p and os.path.exists(p):
                                try: os.remove(p)
                                except: pass
                        st.session_state.films = [f for f in st.session_state.films if f["id"] != film["id"]]
                        st.success(f"{film['titre']} supprimé!")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                st.divider()

    with t3:
        for ab in st.session_state.abonnes:
            st.write(f"{ab['nom']} - {ab['type']} - {ab['fin']}")

else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.info("**SIMPLE 3500F**\n✅ HD")
    with c2: st.success("**PLUS 5000F**\n✅ 4K\n✅ Demande\n✅ Réservation 24h\n✅ Assistance 24h/24")
    with st.form("ab_final"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c})
            st.success(f"{nom} actif jusqu'au {fin}")
