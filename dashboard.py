import streamlit as st
from datetime import datetime, timedelta, date
import random, os, base64

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

GENRES_COMPLETS = ["Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", "Policier", "Romance", "Science-fiction", "Thriller", "Western"]

if "intro_done_v18" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:9999999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 3.2s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;"><div style="flex:1;background:#009543;"></div><div style="flex:1;background:#FBDE4A;"></div><div style="flex:1;background:#DC241F;"></div></div>
        <h1 style="z-index:10;color:white;font-size:58px;font-weight:900;">CONGOSTREAM</h1>
    </div>
    <style>@keyframes fadeOut{to{opacity:0;visibility:hidden;}}</style>
    """, unsafe_allow_html=True)
    st.session_state.intro_done_v18 = True

st.markdown("""
<style>
.stApp { background:#000; color:white; }
.film-card { background:#111; border-radius:10px; overflow:hidden; border:1px solid #222; }
.film-card:hover { border-color:white; transform:scale(1.04); transition:0.25s; }
.film-title { padding:8px; font-weight:700; font-size:12px; text-align:center; background:#181818; }
.glass-nav { position:fixed; top:15px; left:15px; z-index:1000; background: rgba(255,255,255,0.12); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); border:1px solid rgba(255,255,255,0.25); border-radius:14px; padding:8px 14px; }
.glass-desc { background: rgba(0,0,0,0.35); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); border:1px solid rgba(255,255,255,0.18); border-radius:16px; padding:18px; }
.mirror-lecture { background: rgba(255,255,255,0.18); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border:1px solid rgba(255,255,255,0.35); color:white; padding:12px 32px; border-radius:30px; font-weight:900; box-shadow:0 8px 32px rgba(0,0,0,0.5); }
.hero-wrap { position:relative; width:100%; height:88vh; overflow:hidden; margin:-70px -60px 25px -60px; background:#000; }
header{visibility:hidden;}
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

def video_base64(path):
    if path and os.path.exists(path):
        try:
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return f"data:video/mp4;base64,{data}"
        except: return None
    return None

# MENU GLASS 3 TRAITS EN AVANT SUR BANDE ANNONCE
st.markdown('<div class="glass-nav">', unsafe_allow_html=True)
col_ham, col_logo = st.columns([1,4])
with col_ham:
    if st.button("☰", key="hamburger"):
        st.session_state.menu_open = not st.session_state.menu_open
with col_logo:
    st.markdown('<span style="color:#E50914; font-weight:900; font-size:22px; margin-left:8px;">CONGOSTREAM</span>', unsafe_allow_html=True)
if st.session_state.menu_open:
    menu_choice = st.radio("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed")
else:
    menu_choice = st.session_state.get("last_menu", "Accueil")
st.markdown('</div>', unsafe_allow_html=True)

if 'menu_choice' in locals():
    st.session_state.last_menu = menu_choice
    menu = menu_choice
else:
    menu = st.session_state.get("last_menu", "Accueil")

# DETAIL FILM - BANDE ANNONCE AVEC LECTURE MIROIR
if st.session_state.selected_film and menu == "Accueil":
    film = next((f for f in st.session_state.films if f["id"] == st.session_state.selected_film), None)
    if film:
        if st.button("⬅️ Retour"):
            st.session_state.selected_film=None; st.session_state.playing_film=False; st.rerun()

        if st.session_state.playing_film:
            if film.get("film_path") and os.path.exists(film["film_path"]):
                vb = video_base64(film["film_path"])
                if vb:
                    st.markdown(f'<video src="{vb}" controls autoplay style="width:100%; border-radius:12px;"></video>', unsafe_allow_html=True)
                else:
                    st.video(film["film_path"])
            else: st.error("Film complet pas disponible")
        else:
            # Bande annonce qui joue quand on clic sur film
            vb_trailer = video_base64(film.get("trailer_path"))
            st.markdown('<div style="position:relative; width:100%;">', unsafe_allow_html=True)
            if vb_trailer:
                st.markdown(f'<video src="{vb_trailer}" autoplay muted controls style="width:100%; border-radius:12px; max-height:70vh; object-fit:cover;"></video>', unsafe_allow_html=True)
            else:
                if film.get("trailer_path") and os.path.exists(film["trailer_path"]): st.video(film["trailer_path"])

            # BOUTON LECTURE EFFET MIROIR SUR LA BANDE ANNONCE
            st.markdown('<div style="position:absolute; bottom:30px; right:30px; z-index:10;">', unsafe_allow_html=True)
            if st.button("▶️ LECTURE", key="lecture_miroir_detail"):
                if "Simple" in st.session_state.user_tier or "Plus" in st.session_state.user_tier:
                    if film.get("qualite")=="4K" and "Plus" not in st.session_state.user_tier:
                        st.warning("🔒 4K réservé PLUS")
                    else:
                        st.session_state.playing_film=True; st.rerun()
                else:
                    st.error("🔒 Abonnement requis")
            st.markdown('</div></div>', unsafe_allow_html=True)

            # DESCRIPTION EFFET GLASS
            st.markdown(f"""
            <div class="glass-desc" style="margin-top:15px;">
                <h2 style="margin:0;">{film['titre']}</h2>
                <p style="color:#ccc; margin:5px 0;">{film['genre']} • {film['categorie']} • {film['annee']} • {film.get('qualite','HD')}</p>
                <p style="color:#eee;">{film.get('desc','')}</p>
            </div>
            """, unsafe_allow_html=True)

# ACCUEIL AVEC BANDE ANNONCE FORTE AUTOPLAY
elif menu == "Accueil":
    if st.session_state.films:
        hero = st.session_state.films[0]
        vb_hero = video_base64(hero.get("trailer_path"))
        st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
        if vb_hero:
            # AUTOPLAY FIX
            st.markdown(f"""
            <video autoplay muted loop playsinline style="width:100%; height:100%; object-fit:cover;">
                <source src="{vb_hero}" type="video/mp4">
            </video>
            <div style="position:absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(to top, #000 10%, transparent 70%), linear-gradient(to right, #000 25%, transparent 65%);"></div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"<img src='{hero.get('image_path','https://via.placeholder.com/1200x800')}' style='width:100%; height:100%; object-fit:cover;'>", unsafe_allow_html=True)

        # DESCRIPTION GLASS DEVANT BANDE ANNONCE
        st.markdown(f"""
            <div style="position:absolute; bottom:50px; left:50px; max-width:520px; z-index:5;">
                <div class="glass-desc">
                    <h1 style="font-size:48px; font-weight:900; margin:0; line-height:1;">{hero['titre']}</h1>
                    <p style="color:#ddd; margin:8px 0;">{hero['genre']} • {hero['annee']} • {hero.get('qualite','HD')}</p>
                    <p style="color:#eee; font-size:14px;">{hero.get('desc','')[:150]}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ LECTURE", key="hero_lecture_glass"):
            st.session_state.selected_film = hero["id"]
            st.session_state.playing_film = True
            st.rerun()
    else:
        st.info("Upload ton premier film dans Espace Associé pour voir la bande annonce forte à l'entrée")

    st.markdown("### Parcourir")
    cols = st.columns(5)
    for i, film in enumerate(st.session_state.films):
        with cols[i % 5]:
            st.markdown('<div class="film-card">', unsafe_allow_html=True)
            if film.get("image_path") and os.path.exists(film["image_path"]): st.image(film["image_path"], use_container_width=True)
            else: st.image("https://via.placeholder.com/300x450/111/E50914?text=CONGOSTREAM", use_container_width=True)
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
        with st.form("pub_v18", clear_on_submit=True):
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
            trailer_file = st.file_uploader("Bande Annonce Forte * (autoplay entrée)", type=["mp4","mov","mkv","avi"])
            film_file = st.file_uploader("Film Complet", type=["mp4","mkv","mov","avi"]) if not is_annonce else None
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
            if st.button(f"🗑️ Supprimer {film['titre']}", key=f"del_{film['id']}"):
                st.session_state.films = [f for f in st.session_state.films if f["id"]!= film["id"]]; st.rerun()
else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    with st.form("ab_v18"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c})
            st.success(f"Actif jusqu'au {fin}")
