import streamlit as st
from datetime import date, datetime
import random, os, json, tempfile
import cloudinary
import cloudinary.uploader

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

CLOUD_OK=False
try:
    cloudinary.config(
        cloud_name=st.secrets["cloudinary"]["cloud_name"],
        api_key=st.secrets["cloudinary"]["api_key"],
        api_secret=st.secrets["cloudinary"]["api_secret"],
        secure=True
    )
    CLOUD_OK=True
except: CLOUD_OK=False

def upload_cloud(file_obj, folder):
    if not file_obj or not CLOUD_OK: return None
    try:
        suffix=os.path.splitext(file_obj.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_obj.getvalue())
            tmp_path=tmp.name
        res=cloudinary.uploader.upload(tmp_path, resource_type="auto", folder=folder, chunk_size=6000000)
        os.remove(tmp_path)
        return res.get("secure_url")
    except Exception as e:
        st.error(f"Cloudinary: {e}"); return None

GENRES=["Tous","Action","Animation","Aventure","Biopic","Comédie","Documentaire","Drame","Horreur","Erotique","Espionnage","Fantastique","Guerre","Policier","Romance","Sci-Fi","Thriller"]

st.markdown("""
<style>
.stApp{background:#000;color:white;}
/* LOGO TOUT EN HAUT DANS ZONE BLANCHE */
.glass-nav{position:fixed;top:0;left:0;right:0;z-index:99999;background:rgba(0,0,0,0.85);backdrop-filter:blur(15px);border-bottom:1px solid rgba(255,255,255,0.15);padding:8px 15px;display:flex;align-items:center;justify-content:space-between;}
.logo-text{color:#E50914;font-weight:900;font-size:22px;letter-spacing:1px;}
.genre-container{position:fixed;top:42px;left:0;right:0;z-index:99998;background:rgba(0,0,0,0.9)!important;padding:8px 15px;display:flex;gap:8px;overflow-x:auto;white-space:nowrap;scrollbar-width:none;border-bottom:1px solid rgba(255,255,255,0.05);}
.genre-container::-webkit-scrollbar{display:none;}
div[data-testid="stSegmentedControl"]{background:transparent!important;}
div[data-testid="stSegmentedControl"] > div{background:transparent!important;gap:8px!important;margin-top:0!important;}
button[data-testid="stBaseButton-pills"]{background:rgba(255,255,255,0.15)!important;border:1px solid rgba(255,255,255,0.2)!important;border-radius:20px!important;color:white!important;backdrop-filter:blur(10px);padding:4px 12px!important;font-size:13px!important;}
button[data-testid="stBaseButton-pills"][data-active="true"]{background:#E50914!important;border-color:#E50914!important;}
div[data-testid="stMain"]{padding-top:0!important;}
div.block-container{padding-top:88px!important;padding-bottom:0!important;}
.glass-desc{background:rgba(15,15,15,0.75);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.18);border-radius:16px;padding:20px;margin-top:-30px;position:relative;z-index:5;max-width:650px;}
.film-card{max-width:900px;margin:20px auto;background:#111;border-radius:16px;overflow:hidden;border:1px solid #222;}
.admin-card{background:#111;border:1px solid #333;border-radius:12px;padding:15px;margin:12px 0;}
.publi-date{color:#888;font-size:12px;margin-top:5px;font-style:italic;}
header{visibility:hidden;}
video{border-radius:12px;margin-top:0!important;}
</style>
""", unsafe_allow_html=True)

DATA_FILE="congo_films_cloud.json"
if "films" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,"r") as f: st.session_state.films=json.load(f)
        except: st.session_state.films=[]
    else: st.session_state.films=[]
if "selected_film" not in st.session_state: st.session_state.selected_film=None
if "playing_film" not in st.session_state: st.session_state.playing_film=False
if "menu_open" not in st.session_state: st.session_state.menu_open=False
if "current_page" not in st.session_state: st.session_state.current_page="Accueil"
if "hero_index" not in st.session_state: st.session_state.hero_index=0
if "genre_filter" not in st.session_state: st.session_state.genre_filter="Tous"
if "edit_id" not in st.session_state: st.session_state.edit_id=None

def save_films():
    with open(DATA_FILE,"w") as f: json.dump(st.session_state.films,f,indent=2,default=str)

def video_auto(url, height="550px"):
    html=f"""<video autoplay loop playsinline controls style="width:100%; height:{height}; object-fit:cover; background:#000;"><source src="{url}" type="video/mp4"></video>"""
    st.markdown(html, unsafe_allow_html=True)

def video_16_9(url):
    html=f"""<div style="width:100%; aspect-ratio:16/9; background:#000; border-radius:16px; overflow:hidden;"><video autoplay loop playsinline controls style="width:100%; height:100%; object-fit:cover;"><source src="{url}" type="video/mp4"></video></div>"""
    st.markdown(html, unsafe_allow_html=True)

# LOGO DANS ZONE BLANCHE EN HAUT
st.markdown('<div class="glass-nav">', unsafe_allow_html=True)
col_menu, col_logo, col_vide = st.columns([1,3,1])
with col_menu:
    if st.button("☰"):
        st.session_state.menu_open=not st.session_state.menu_open
with col_logo:
    st.markdown('<div class="logo-text">CONGOSTREAM</div>', unsafe_allow_html=True)
with col_vide:
    st.markdown("")
if st.session_state.menu_open:
    choix=st.radio("",["Accueil","Espace Associé","S'abonner"],label_visibility="collapsed")
    st.session_state.current_page=choix
    if st.button("Fermer ✕"): st.session_state.menu_open=False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.current_page=="Accueil":
    st.markdown('<div class="genre-container">', unsafe_allow_html=True)
    selected = st.pills("", GENRES, default=st.session_state.genre_filter, selection_mode="single", label_visibility="collapsed")
    if selected:
        st.session_state.genre_filter=selected
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

menu=st.session_state.current_page

if st.session_state.selected_film and menu=="Accueil":
    film=next((f for f in st.session_state.films if f["id"]==st.session_state.selected_film),None)
    if film:
        if st.button("⬅️ Retour"): st.session_state.selected_film=None; st.session_state.playing_film=False; st.rerun()
        if st.session_state.playing_film:
            if film.get("film_url"): video_auto(film["film_url"], "600px")
            else:
                if film.get("trailer_url"): video_auto(film["trailer_url"], "600px")
        else:
            if film.get("trailer_url"): video_auto(film["trailer_url"], "600px")
            elif film.get("image_url"): st.image(film["image_url"], use_container_width=True)
            if st.button("▶️ LECTURE", use_container_width=True, type="primary"):
                st.session_state.playing_film=True; st.rerun()
            st.markdown(f'<div class="glass-desc"><h2>{film["titre"]}</h2><p>{film["genre"]} • {film["annee"]}</p><p>{film.get("desc","")}</p></div>', unsafe_allow_html=True)

elif menu=="Accueil":
    filtered=[f for f in st.session_state.films if st.session_state.genre_filter=="Tous" or f["genre"]==st.session_state.genre_filter]
    if filtered:
        hero = filtered[st.session_state.hero_index % len(filtered)]
        if hero.get("trailer_url"): video_auto(hero["trailer_url"], "550px")
        elif hero.get("image_url"): st.image(hero["image_url"], use_container_width=True)
        col1,col2=st.columns([4,1])
        with col2:
            if st.button("🔐 Espace Associé", key="assoc_top_right"):
                st.session_state.current_page="Espace Associé"; st.rerun()
        with col1:
            if st.button("▶️ LECTURE", key="hero_play", use_container_width=True, type="primary"):
                st.session_state.selected_film=hero["id"]; st.session_state.playing_film=True; st.rerun()
            if st.button("⏭️ Film suivant", use_container_width=True):
                st.session_state.hero_index+=1; st.rerun()
        st.markdown(f'<div class="glass-desc"><h1 style="font-size:36px;font-weight:900;margin:0;">{hero["titre"]}</h1><p>{hero["genre"]} • {hero["annee"]}</p></div>', unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align:center;'>🎬 Bandes annonces - 16:9</h2>", unsafe_allow_html=True)
    for film in filtered:
        st.markdown('<div class="film-card">', unsafe_allow_html=True)
        if film.get("trailer_url"): video_16_9(film["trailer_url"])
        elif film.get("image_url"): st.image(film["image_url"], use_container_width=True)
        st.markdown(f'<div style="padding:15px;"><h3>{film["titre"]}</h3>', unsafe_allow_html=True)
        if st.button(f"Voir {film['titre']}", key=f"voir_{film['id']}", use_container_width=True):
            st.session_state.selected_film=film["id"]; st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

elif menu=="Espace Associé":
    st.title("🔐 Espace Associé")
    if CLOUD_OK: st.success("✅ Cloudinary OK")
    else: st.error("❌ Vérifie Secrets")
    code=st.text_input("Code d'accès", type="password", placeholder="RolVie2002")
    if code and code!="RolVie2002" and code!="": st.error("Mauvais code"); st.stop()
    if code=="RolVie2002":
        tab1, tab2 = st.tabs(["📤 Publier Nouveau", "🛠️ Gérer Contenus"])
        with tab1:
            with st.form("pub", clear_on_submit=True):
                titre=st.text_input("Titre *")
                c1,c2=st.columns(2)
                with c1: genre=st.selectbox("Genre", GENRES[1:])
                with c2: annee=st.text_input("Année","2026")
                desc=st.text_area("Description")
                trailer=st.file_uploader("Bande Annonce * (vidéo)", type=["mp4","mov","mkv"])
                film_c=st.file_uploader("Film Complet (vidéo optionnel)", type=["mp4","mkv","mov"])
                affiche=st.file_uploader("🖼️ Pochette / Affiche du film (image)", type=["jpg","jpeg","png","webp"])
                if st.form_submit_button("☁️ PUBLIER", use_container_width=True, type="primary"):
                    if titre and trailer and CLOUD_OK:
                        with st.spinner("Upload Cloudinary..."):
                            t_url=upload_cloud(trailer,"congo_trailers")
                            f_url=upload_cloud(film_c,"congo_films") if film_c else None
                            i_url=upload_cloud(affiche,"congo_images") if affiche else None
                            if t_url:
                                now = datetime.now()
                                st.session_state.films.append({
                                    "id":random.randint(1000,99999),
                                    "titre":titre,
                                    "genre":genre,
                                    "annee":annee,
                                    "desc":desc,
                                    "trailer_url
