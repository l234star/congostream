import streamlit as st
from datetime import datetime, timedelta, date
import random, os

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

GENRES_COMPLETS = ["Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", "Policier", "Romance", "Science-fiction", "Thriller", "Western"]

if "intro_done_v19" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:9999999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 3s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;"><div style="flex:1;background:#009543;"></div><div style="flex:1;background:#FBDE4A;"></div><div style="flex:1;background:#DC241F;"></div></div>
        <h1 style="z-index:10;color:white;font-size:58px;font-weight:900;">CONGOSTREAM</h1>
    </div>
    <style>@keyframes fadeOut{to{opacity:0;visibility:hidden;}}</style>
    """, unsafe_allow_html=True)
    st.session_state.intro_done_v19 = True

st.markdown("""
<style>
.stApp { background:#000; color:white; }
.film-card { background:#111; border-radius:10px; overflow:hidden; border:1px solid #222; }
.film-card:hover { border-color:#E50914; transform:scale(1.04); transition:0.25s; }
.film-title { padding:8px; font-weight:700; font-size:12px; text-align:center; background:#181818; }
.glass-nav { position:fixed; top:12px; left:12px; z-index:9999; background: rgba(255,255,255,0.15); backdrop-filter: blur(15px); border:1px solid rgba(255,255,255,0.25); border-radius:14px; padding:6px 12px; }
.glass-desc { background: rgba(20,20,20,0.55); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); border:1px solid rgba(255,255,255,0.18); border-radius:16px; padding:18px; margin-top:-100px; position:relative; z-index:5; max-width:600px; }
header{visibility:hidden;}
video { border-radius:12px; }
</style>
""", unsafe_allow_html=True)

os.makedirs("videos", exist_ok=True); os.makedirs("trailers", exist_ok=True); os.makedirs("images", exist_ok=True)

if "films" not in st.session_state: st.session_state.films = []
if "abonnes" not in st.session_state: st.session_state.abonnes = []
if "selected_film" not in st.session_state: st.session_state.selected_film = None
if "user_tier" not in st.session_state: st.session_state.user_tier = "Gratuit"
if "playing_film" not in st.session_state: st.session_state.playing_film = False
if "menu_open" not in st.session_state: st.session_state.menu_open = False

def save_file(f, folder):
    if f:
        p = os.path.join(folder, f.name)
        with open(p, "wb") as out: out.write(f.getbuffer())
        return p
    return None

# MENU 3 TRAITS GLASS
st.markdown('<div class="glass-nav">', unsafe_allow_html=True)
c_ham, c_logo = st.columns([1,4])
with c_ham:
    if st.button("☰", key="ham"):
        st.session_state.menu_open = not st.session_state.menu_open
with c_logo:
    st.markdown('<span style="color:#E50914; font-weight:900; font-size:20px;">CONGOSTREAM</span>', unsafe_allow_html=True)
if st.session_state.menu_open:
    menu = st.radio("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed", key="menu_radio")
    st.session_state.last_menu = menu
else:
    menu = st.session_state.get("last_menu", "Accueil")
st.markdown('</div>', unsafe_allow_html=True)

# DETAIL FILM
if st.session_state.selected_film and menu == "Accueil":
    film = next((f for f in st.session_state.films if f["id"] == st.session_state.selected_film), None)
    if film:
        if st.button("⬅️ Retour"):
            st.session_state.selected_film=None; st.session_state.playing_film=False; st.rerun()

        if st.session_state.playing_film:
            if film.get("film_path") and os.path.exists(film["film_path"]):
                st.video(film["film_path"], autoplay=True)
            else:
                st.error("Film complet pas disponible")
                if st.button("Revoir bande annonce"): st.session_state.playing_film=False; st.rerun()
        else:
            # BANDE ANNONCE QUI SE LANCE QUAND ON CLIC SUR FILM
            if film.get("trailer_path") and os.path.exists(film["trailer_path"]):
                st.video(film["trailer_path"], autoplay=True)
            # BOUTON LECTURE EFFET MIROIR SUR LA BANDE ANNONCE
            col_m1, col_m2, col_m3 = st.columns([2,1,2])
            with col_m2:
                if st.button("▶️ LECTURE", key="lecture_miroir", use_container_width=True):
                    if "Simple" in st.session_state.user_tier or "Plus" in st.session_state.user_tier:
                        st.session_state.playing_film=True; st.rerun()
                    else:
                        st.error("🔒 Abonnement requis")

            st.markdown(f"""
            <div class="glass-desc">
                <h2 style="margin:0;">{film['titre']}</h2>
                <p style="color:#ccc;">{film['genre']} • {film['categorie']} • {film['annee']} • {film.get('qualite','HD')}</p>
                <p>{film.get('desc','')}</p>
            </div>
            """, unsafe_allow_html=True)

elif menu == "Accueil":
    # BANDE ANNONCE FORTE AUTOPLAY A L'ENTREE
    if st.session_state.films:
        hero = st.session_state.films[0]
        st.markdown("### 🔥 À la une")
        if hero.get("trailer_path") and os.path.exists(hero["trailer_path"]):
            # ICI CA AUTOPLAY VRAIMENT
            st.video(hero["trailer_path"], autoplay=True, muted=True, loop=True)
            # DESCRIPTION GLASS DEVANT
            st.markdown(f"""
            <div class="glass-desc">
                <h1 style="font-size:42px; font-weight:900; margin:0;">{hero['titre']}</h1>
                <p style="color:#ccc;">{hero['genre']} • {hero['annee']} • {hero.get('qualite','HD')}</p>
                <p>{hero.get('desc','')}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶️ LECTURE", key="hero_lec"):
                st.session_state.selected_film = hero["id"]
                st.session_state.playing_film = True
                st.rerun()
        else:
            if hero.get("image_path") and os.path.exists(hero.get("image_path")):
                st.image(hero["image_path"], use_container_width=True)
            st.warning("Hero n'a pas de bande annonce - upload une bande annonce pour autoplay")
    else:
        st.markdown("""
        <div style="background:#111; padding:80px; text-align:center; border-radius:12px;">
            <h1>Bienvenue sur CONGOSTREAM</h1>
            <p>Upload ton premier film dans Espace Associé pour voir la bande annonce forte ici</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🎬 Parcourir - Clique sur un film")
    cols = st.columns(4)
    for i, film in enumerate(st.session_state.films):
        with cols[i % 4]:
            st.markdown('<div class="film-card">', unsafe_allow_html=True)
            if film.get("image_path") and os.path.exists(film["image_path"]):
                st.image(film["image_path"], use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x450/111/E50914?text=CONGOSTREAM", use_container_width=True)
            st.markdown(f"<div class='film-title'>{film['titre']}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Voir", key=f"voir_{film['id']}", use_container_width=True):
                st.session_state.selected_film = film["id"]; st.session_state.playing_film=False; st.rerun()

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
        with st.form("pub_v19", clear_on_submit=True):
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
            trailer_file = st.file_uploader("Bande Annonce Forte * (celle-ci va autoplay à l'accueil)", type=["mp4","mov","mkv","avi"])
            film_file = st.file_uploader("Film Complet", type=["mp4","mkv","mov","avi"]) if not is_annonce else None
            image_file = st.file_uploader("Affiche (image dans cadre)", type=["jpg","png","jpeg","webp"])
            if st.form_submit_button("🔓 ENTRÉE - PUBLIER", use_container_width=True):
                if titre and trailer_file:
                    tp = save_file(trailer_file, "trailers")
                    fp = save_file(film_file, "videos") if film_file else None
                    ip = save_file(image_file, "images") if image_file else None
                    st.session_state.films.append({"id": random.randint(100,99999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee, "desc":desc, "trailer_path":tp, "film_path":fp, "image_path":ip, "qualite":"4K" if "4K" in qualite else "HD", "is_annonce":is_annonce, "date_sortie":date_sortie})
                    st.success(f"✅ {titre} publié! Va à l'accueil, la bande annonce va se lancer auto!"); st.balloons()
                else: st.warning("Titre + Bande annonce obligatoire")
    with t2:
        for film in st.session_state.films[:]:
            if st.button(f"🗑️ Supprimer {film['titre']}", key=f"del_{film['id']}"):
                st.session_state.films = [f for f in st.session_state.films if f["id"]!= film["id"]]; st.rerun()
else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    with st.form("ab_v19"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c})
            st.success(f"Actif jusqu'au {fin}")
