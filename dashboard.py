import streamlit as st
from datetime import datetime, timedelta, date
import random, os

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

GENRES_COMPLETS = ["Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", "Policier", "Romance", "Science-fiction", "Thriller", "Western"]

if "intro_done_v17" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:9999999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 3.5s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;"><div style="flex:1;background:#009543;"></div><div style="flex:1;background:#FBDE4A;"></div><div style="flex:1;background:#DC241F;"></div></div>
        <h1 style="z-index:10;color:white;font-size:58px;font-weight:900;">CONGOSTREAM</h1>
    </div>
    <style>@keyframes fadeOut{to{opacity:0;visibility:hidden;}}</style>
    """, unsafe_allow_html=True)
    st.session_state.intro_done_v17 = True

st.markdown("""
<style>
.stApp { background:#000; color:white; }
.film-card { background:#111; border-radius:8px; overflow:hidden; border:1px solid #222; }
.film-card:hover { border-color:white; transform:scale(1.05); transition:0.3s; }
.film-title { padding:8px; font-weight:700; font-size:13px; text-align:center; background:#181818; }
.hero-video { position:relative; width:100%; height:85vh; overflow:hidden; margin:-70px -60px 20px -60px; background:#000; }
.hero-video video { width:100%; height:100%; object-fit:cover; }
.hero-overlay { position:absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(to top, #000 0%, transparent 50%), linear-gradient(to right, #000 20%, transparent 60%); }
.mirror-btn { background: rgba(255,255,255,0.15); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border:1px solid rgba(255,255,255,0.3); color:white; padding:12px 28px; border-radius:30px; font-weight:900; font-size:16px; box-shadow:0 8px 32px rgba(0,0,0,0.4); cursor:pointer; }
.mirror-btn:hover { background: rgba(229,9,20,0.8); transform:scale(1.05); }
.video-wrapper { position:relative; width:100%; border-radius:12px; overflow:hidden; }
.lecture-on-video { position:absolute; bottom:25px; right:25px; z-index:10; }
header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

os.makedirs("videos", exist_ok=True); os.makedirs("trailers", exist_ok=True); os.makedirs("images", exist_ok=True)

if "films" not in st.session_state: st.session_state.films = []
if "abonnes" not in st.session_state: st.session_state.abonnes = []
if "selected_film" not in st.session_state: st.session_state.selected_film = None
if "user_tier" not in st.session_state: st.session_state.user_tier = "Gratuit"
if "playing_film" not in st.session_state: st.session_state.playing_film = False

def save_file(f, folder):
    if f:
        p = os.path.join(folder, f.name)
        with open(p, "wb") as out: out.write(f.getbuffer())
        return p
    return None

c1, c2 = st.columns([5,1])
with c1: st.markdown('<div style="color:#E50914; font-weight:900; font-size:32px;">CONGOSTREAM</div>', unsafe_allow_html=True)
with c2: menu = st.selectbox("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed")

# DETAIL QUAND ON CLIC SUR UN FILM
if st.session_state.selected_film and menu == "Accueil":
    film = next((f for f in st.session_state.films if f["id"] == st.session_state.selected_film), None)
    if film:
        if st.button("⬅️ Retour"):
            st.session_state.selected_film=None
            st.session_state.playing_film=False
            st.rerun()

        # SI LECTURE = FILM COMPLET
        if st.session_state.playing_film:
            if film.get("film_path") and os.path.exists(film["film_path"]):
                st.video(film["film_path"])
                if st.button("⏸️ Revoir bande annonce"): st.session_state.playing_film=False; st.rerun()
            else: st.error("Film complet pas disponible")
        else:
            # BANDE ANNONCE AVEC BOUTON LECTURE EFFET MIROIR DESSUS
            st.markdown(f"<h2 style='margin:10px 0;'>{film['titre']} • {film['genre']} • {film['annee']}</h2>", unsafe_allow_html=True)

            if film.get("trailer_path") and os.path.exists(film["trailer_path"]):
                st.markdown('<div class="video-wrapper">', unsafe_allow_html=True)
                st.video(film["trailer_path"])
                st.markdown('</div>', unsafe_allow_html=True)

            # BOUTON LECTURE EFFET MIROIR SUR LA BANDE ANNONCE
            col1, col2, col3 = st.columns([2,1,2])
            with col2:
                st.markdown('<div style="margin-top:-80px; position:relative; z-index:10; text-align:center;">', unsafe_allow_html=True)
                if st.button("▶️ LECTURE", key="lecture_miroir", use_container_width=True):
                    if "Simple" in st.session_state.user_tier or "Plus" in st.session_state.user_tier:
                        if film.get("qualite")=="4K" and "Plus" not in st.session_state.user_tier:
                            st.warning("🔒 4K réservé PLUS 5000F")
                        else:
                            st.session_state.playing_film=True
                            st.rerun()
                    else:
                        st.error("🔒 Abonnement requis pour regarder le film")
                        st.info("Va dans S'abonner")
                st.markdown('</div>', unsafe_allow_html=True)

            if film.get("is_annonce") and film.get("date_sortie"):
                st.caption(f"Sortie prévue le {film['date_sortie'].strftime('%d/%m/%Y')}")

elif menu == "Accueil":
    # BANDE ANNONCE FORTE QUI SE LIT AUTO DES L'ENTREE
    if st.session_state.films:
        hero = st.session_state.films[0]
        if hero.get("trailer_path") and os.path.exists(hero.get("trailer_path")):
            # HERO AUTOPLAY
            st.markdown(f"""
            <div class="hero-video">
                <video autoplay muted loop playsinline>
                    <source src="{hero['trailer_path']}" type="video/mp4">
                </video>
                <div class="hero-overlay"></div>
                <div style="position:absolute; bottom:60px; left:60px; max-width:500px;">
                    <h1 style="font-size:55px; font-weight:900; margin:0; line-height:1;">{hero['titre']}</h1>
                    <p style="color:#ccc; margin:10px 0;">{hero['genre']} • {hero['annee']} • {hero.get('qualite','HD')}</p>
                    <p style="color:#ddd;">{hero.get('desc','')[:120]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Lecture sur hero aussi avec effet miroir
            col_hero = st.columns([1,1,4])
            with col_hero[0]:
                if st.button("▶️ LECTURE", key="hero_lecture"):
                    st.session_state.selected_film = hero["id"]
                    st.session_state.playing_film = True
                    st.rerun()
        else:
            if hero.get("image_path") and os.path.exists(hero.get("image_path")):
                st.image(hero["image_path"], use_container_width=True)
    else:
        st.markdown("""
        <div class="hero-video" style="display:flex;align-items:center;justify-content:center; background:#111;">
            <h1>CONGOSTREAM - Upload ton premier film dans Espace Associé</h1>
        </div>
        """, unsafe_allow_html=True)

    tier = st.selectbox("👤 Mon forfait", ["Gratuit", "Simple - 3500F", "Plus - 5000F"], label_visibility="collapsed")
    st.session_state.user_tier = tier

    if st.session_state.films:
        st.markdown("### Parcourir")
        cols = st.columns(5)
        for i, film in enumerate(st.session_state.films):
            with cols[i % 5]:
                st.markdown('<div class="film-card">', unsafe_allow_html=True)
                if film.get("image_path") and os.path.exists(film["image_path"]):
                    st.image(film["image_path"], use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/300x450/111/E50914?text=CONGOSTREAM", use_container_width=True)
                st.markdown(f"<div class='film-title'>{film['titre']}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                if st.button("Voir", key=f"voir_{film['id']}", use_container_width=True):
                    st.session_state.selected_film = film["id"]
                    st.session_state.playing_film = False
                    st.rerun()

elif menu == "Espace Associé":
    st.title("Espace Associé")
    if not st.session_state.get("admin"):
        code = st.text_input("Code", type="password", placeholder="RolVie2002")
        if st.button("🔓 ENTRÉE", use_container_width=True):
            if code == "RolVie2002": st.session_state["admin"]=True; st.rerun()
            else: st.error("Mauvais code")
        st.stop()
    if st.button("Déconnexion"): st.session_state["admin"]=False; st.rerun()
    t1, t2 = st.tabs(["📤 Publier", "🗑️ Supprimer"])
    with t1:
        with st.form("pub_v17", clear_on_submit=True):
            titre = st.text_input("Titre *")
            is_annonce = st.checkbox("🔔 Annonce avec date")
            cA, cB = st.columns(2)
            with cA:
                categorie = st.selectbox("Catégorie", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre *", GENRES_COMPLETS)
            with cB:
                annee = st.text_input("Année", "2026")
                qualite = st.selectbox("Qualité", ["HD - Simple", "4K - Plus"])
                date_sortie = st.date_input("📅 Date sortie", value=date.today()+timedelta(days=7)) if is_annonce else None
            desc = st.text_area("Description")
            trailer_file = st.file_uploader("Bande Annonce Forte * (sera autoplay à l'entrée)", type=["mp4","mov","mkv","avi"])
            film_file = st.file_uploader("Film Complet (lu via bouton Lecture)", type=["mp4","mkv","mov","avi"]) if not is_annonce else None
            image_file = st.file_uploader("Affiche", type=["jpg","png","jpeg","webp"])
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
            col1, col2 = st.columns([4,1])
            with col1: st.write(f"**{film['titre']}**")
            with col2:
                if st.button("🗑️", key=f"del_{film['id']}"):
                    st.session_state.films = [f for f in st.session_state.films if f["id"]!= film["id"]]; st.rerun()
else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    with st.form("ab_v17"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c})
            st.success(f"Actif jusqu'au {fin}")
