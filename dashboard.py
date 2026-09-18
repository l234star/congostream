import streamlit as st
from datetime import date
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
.glass-nav{position:fixed;top:10px;left:10px;z-index:99999;background:rgba(255,255,255,0.12);backdrop-filter:blur(15px);border:1px solid rgba(255,255,255,0.25);border-radius:14px;padding:8px 14px;display:flex;align-items:center;gap:10px;}
.genre-bar{position:fixed;top:65px;left:10px;right:10px;z-index:99998;display:flex;gap:8px;overflow-x:auto;white-space:nowrap;padding:10px 5px;background:linear-gradient(to bottom, rgba(0,0,0,0.9), transparent);}
.genre-pill{background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.2);border-radius:20px;padding:6px 14px;color:white;font-size:13px;cursor:pointer;}
.genre-pill.active{background:#E50914;border-color:#E50914;}
.glass-corner-btn{position:absolute;top:15px;right:15px;z-index:50;background:rgba(255,255,255,0.15);backdrop-filter:blur(15px);border:1px solid rgba(255,255,255,0.3);border-radius:10px;padding:8px 14px;color:white;font-weight:600;font-size:13px;}
.hero-wrapper{position:relative;width:100%;}
.glass-desc{background:rgba(15,15,15,0.75);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.18);border-radius:16px;padding:20px;margin-top:-30px;position:relative;z-index:5;max-width:650px;}
.film-card{max-width:900px;margin:35px auto;background:#111;border-radius:16px;overflow:hidden;border:1px solid #222;}
header{visibility:hidden;}
video{border-radius:12px;}
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

def save_films():
    with open(DATA_FILE,"w") as f: json.dump(st.session_state.films,f,indent=2,default=str)

def video_auto(url, height="550px"):
    html=f"""<video autoplay loop playsinline controls style="width:100%; height:{height}; object-fit:cover; background:#000;"><source src="{url}" type="video/mp4"></video>"""
    st.markdown(html, unsafe_allow_html=True)

def video_16_9(url):
    html=f"""<div style="width:100%; aspect-ratio:16/9; background:#000; border-radius:16px; overflow:hidden;"><video autoplay loop playsinline controls style="width:100%; height:100%; object-fit:cover;"><source src="{url}" type="video/mp4"></video></div>"""
    st.markdown(html, unsafe_allow_html=True)

# LOGO + MENU 3 TRAITS
st.markdown('<div class="glass-nav">', unsafe_allow_html=True)
c1,c2=st.columns([1,5])
with c1:
    if st.button("☰", key="menu_btn"):
        st.session_state.menu_open=not st.session_state.menu_open
with c2:
    st.markdown('<span style="color:#E50914;font-weight:900;font-size:20px;">CONGOSTREAM</span>', unsafe_allow_html=True)
if st.session_state.menu_open:
    choix=st.radio("",["Accueil","Espace Associé","S'abonner"],label_visibility="collapsed")
    st.session_state.current_page=choix
    if st.button("Fermer ✕"): st.session_state.menu_open=False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# GENRES EN PREMIER PLAN JUSTE SOUS LE LOGO
if st.session_state.current_page=="Accueil":
    genres_html='<div class="genre-bar">'
    for g in GENRES:
        active="active" if g==st.session_state.genre_filter else ""
        genres_html+=f'<span class="genre-pill {active}">{g}</span>'
    genres_html+='</div>'
    st.markdown(genres_html, unsafe_allow_html=True)
    # Boutons cliquables pour filtrer
    cols=st.columns(len(GENRES))
    for i,g in enumerate(GENRES):
        with cols[i]:
            if st.button(g, key=f"genre_{g}", use_container_width=True):
                st.session_state.genre_filter=g
                st.rerun()

menu=st.session_state.current_page
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# DETAIL
if st.session_state.selected_film and menu=="Accueil":
    film=next((f for f in st.session_state.films if f["id"]==st.session_state.selected_film),None)
    if film:
        if st.button("⬅️ Retour"): st.session_state.selected_film=None; st.session_state.playing_film=False; st.rerun()
        if st.session_state.playing_film:
            if film.get("film_url"): video_auto(film["film_url"], "600px")
            else:
                st.warning("Film complet non dispo")
                if film.get("trailer_url"): video_auto(film["trailer_url"], "600px")
        else:
            if film.get("trailer_url"): video_auto(film["trailer_url"], "600px")
            if st.button("▶️ LECTURE", use_container_width=True, type="primary"):
                st.session_state.playing_film=True; st.rerun()
            st.markdown(f'<div class="glass-desc"><h2>{film["titre"]}</h2><p style="color:#aaa;">{film["genre"]} • {film["annee"]}</p><p>{film.get("desc","")}</p></div>', unsafe_allow_html=True)

elif menu=="Accueil":
    filtered=[f for f in st.session_state.films if st.session_state.genre_filter=="Tous" or f["genre"]==st.session_state.genre_filter]
    if filtered:
        hero = filtered[st.session_state.hero_index % len(filtered)]
        # HERO AVEC BOUTON GLASS EN HAUT A DROITE SUR LA BANDE ANNONCE
        st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
        if hero.get("trailer_url"): video_auto(hero["trailer_url"], "550px")
        st.markdown('</div>', unsafe_allow_html=True)

        # BOUTON ESPACE ASSOCIE EN GLASS SUR LA VIDEO - COIN DROIT
        c_hero1,c_hero2=st.columns([4,1])
        with c_hero2:
            if st.button("🔐 Espace Associé", key="assoc_top_right"):
                st.session_state.current_page="Espace Associé"; st.rerun()
        with c_hero1:
            if st.button("▶️ LECTURE", key="hero_play", use_container_width=True, type="primary"):
                st.session_state.selected_film=hero["id"]; st.session_state.playing_film=True; st.rerun()
            if st.button("⏭️ Film suivant", use_container_width=True):
                st.session_state.hero_index+=1; st.rerun()

        st.markdown(f'<div class="glass-desc"><h1 style="font-size:36px;font-weight:900;margin:0;">{hero["titre"]}</h1><p>{hero["genre"]} • {hero["annee"]}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align:center;margin-top:80px;'>Aucun film dans ce genre</h2>", unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align:center;'>🎬 Bandes annonces - Format cinéma 16:9</h2>", unsafe_allow_html=True)
    for film in filtered:
        st.markdown('<div class="film-card">', unsafe_allow_html=True)
        if film.get("trailer_url"): video_16_9(film["trailer_url"])
        elif film.get("image_url"): st.image(film["image_url"], use_container_width=True)
        st.markdown(f'<div style="padding:15px;"><h3>{film["titre"]}</h3><p style="color:#888;">{film["genre"]} • {film["annee"]}</p>', unsafe_allow_html=True)
        if st.button(f"Voir {film['titre']}", key=f"voir_{film['id']}", use_container_width=True):
            st.session_state.selected_film=film["id"]; st.session_state.playing_film=False; st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

elif menu=="Espace Associé":
    st.title("🔐 Espace Associé")
    if CLOUD_OK: st.success("✅ Cloudinary OK")
    else: st.error("❌ Vérifie Secrets")
    code=st.text_input("Code", type="password", placeholder="RolVie2002")
    if code and code!="RolVie2002": st.error("Mauvais code"); st.stop()
    if code=="RolVie2002":
        with st.form("pub", clear_on_submit=True):
            titre=st.text_input("Titre *")
            c1,c2=st.columns(2)
            with c1: genre=st.selectbox("Genre", GENRES[1:])
            with c2: annee=st.text_input("Année","2026")
            desc=st.text_area("Desc")
            trailer=st.file_uploader("Bande Annonce *", type=["mp4","mov","mkv"])
            film_c=st.file_uploader("Film Complet (optionnel)", type=["mp4","mkv","mov"])
            affiche=st.file_uploader("Affiche (optionnel)", type=["jpg","png","jpeg","webp"])
            if st.form_submit_button("☁️ PUBLIER", use_container_width=True, type="primary"):
                if titre and trailer and CLOUD_OK:
                    with st.spinner("Upload..."):
                        t_url=upload_cloud(trailer,"congo_trailers")
                        f_url=upload_cloud(film_c,"congo_films") if film_c else None
                        i_url=upload_cloud(affiche,"congo_images") if affiche else None
                        if t_url:
                            st.session_state.films.append({"id":random.randint(1000,99999),"titre":titre,"genre":genre,"annee":annee,"desc":desc,"trailer_url":t_url,"film_url":f_url,"image_url":i_url,"date":str(date.today())})
                            save_films(); st.success("Publié!"); st.balloons()
                else: st.warning("Titre + Bande annonce obligatoire")
else:
    st.markdown('<h1 style="color:#E50914;">S\'abonner</h1>', unsafe_allow_html=True)
    st.info("MTN 066778924 - 3500F / 5000F")
