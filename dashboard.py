import streamlit as st
from datetime import date
import random, os, json
import cloudinary
import cloudinary.uploader

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

# --- CLOUDINARY ---
try:
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloud_name"],
        api_key = st.secrets["cloudinary"]["api_key"],
        api_secret = st.secrets["cloudinary"]["api_secret"],
        secure=True
    )
    CLOUD_OK = True
except:
    CLOUD_OK = False

GENRES = ["Action","Animation","Aventure","Biopic","Comédie","Documentaire","Drame","Horreur","Erotique","Espionnage","Fantastique","Guerre","Policier","Romance","Science-fiction","Thriller","Western"]

st.markdown("""
<style>
.stApp{background:#000;color:white;}
.glass-nav{position:fixed;top:12px;left:12px;z-index:9999;background:rgba(255,255,255,0.15);backdrop-filter:blur(15px);border:1px solid rgba(255,255,255,0.25);border-radius:14px;padding:6px 12px;}
.glass-desc{background:rgba(20,20,20,0.65);backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,0.18);border-radius:16px;padding:18px;margin-top:-80px;position:relative;z-index:5;max-width:650px;}
header{visibility:hidden;}
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

def save_films():
    with open(DATA_FILE,"w") as f: json.dump(st.session_state.films,f,indent=2,default=str)

def upload_cloud(file_obj, folder):
    if not CLOUD_OK: return None
    try:
        res = cloudinary.uploader.upload_large(file_obj, resource_type="video", folder=folder, chunk_size=6000000)
        return res.get("secure_url")
    except:
        try:
            res = cloudinary.uploader.upload(file_obj, resource_type="auto", folder=folder)
            return res.get("secure_url")
        except Exception as e:
            st.error(f"Erreur Cloudinary: {e}"); return None

# MENU GLASS
st.markdown('<div class="glass-nav">', unsafe_allow_html=True)
c1,c2=st.columns([1,4])
with c1:
    if st.button("☰"): st.session_state.menu_open=not st.session_state.menu_open
with c2:
    st.markdown('<span style="color:#E50914;font-weight:900;font-size:20px;">CONGOSTREAM</span>', unsafe_allow_html=True)
if st.session_state.menu_open:
    menu=st.radio("",["Accueil","Espace Associé","S'abonner"],label_visibility="collapsed")
    st.session_state.last_menu=menu
else:
    menu=st.session_state.get("last_menu","Accueil")
st.markdown('</div>', unsafe_allow_html=True)

# DETAIL FILM
if st.session_state.selected_film and menu=="Accueil":
    film=next((f for f in st.session_state.films if f["id"]==st.session_state.selected_film),None)
    if film:
        if st.button("⬅️ Retour"): st.session_state.selected_film=None; st.session_state.playing_film=False; st.rerun()
        if st.session_state.playing_film:
            if film.get("film_url"): st.video(film["film_url"],autoplay=True)
            else: st.warning("Film complet non uploadé")
        else:
            if film.get("trailer_url"): st.video(film["trailer_url"],autoplay=True)
            if st.button("▶️ LECTURE",use_container_width=True): st.session_state.playing_film=True; st.rerun()
            st.markdown(f'<div class="glass-desc"><h2>{film["titre"]}</h2><p>{film["genre"]} • {film["annee"]}</p><p>{film.get("desc","")}</p></div>', unsafe_allow_html=True)

elif menu=="Accueil":
    if st.session_state.films:
        hero=st.session_state.films[0]
        if hero.get("trailer_url"): st.video(hero["trailer_url"],autoplay=True,muted=True,loop=True)
        st.markdown(f'<div class="glass-desc"><h1 style="font-size:38px;font-weight:900;margin:0;">{hero["titre"]}</h1><p>{hero["genre"]} • {hero["annee"]}</p></div>', unsafe_allow_html=True)
        if st.button("▶️ LECTURE HERO"): st.session_state.selected_film=hero["id"]; st.session_state.playing_film=True; st.rerun()
    st.markdown("### 🎬 Films")
    cols=st.columns(4)
    for i,film in enumerate(st.session_state.films):
        with cols[i%4]:
            if film.get("image_url"): st.image(film["image_url"],use_container_width=True)
            st.write(f"**{film['titre']}**")
            if st.button("Voir",key=f"v_{film['id']}",use_container_width=True):
                st.session_state.selected_film=film["id"]; st.session_state.playing_film=False; st.rerun()

elif menu=="Espace Associé":
    st.title("Espace Associé - Cloudinary")
    if not CLOUD_OK: st.error("⚠️ Ajoute tes clés Cloudinary dans Secrets!")
    code=st.text_input("Code",type="password",placeholder="RolVie2002")
    if code!="" and code!="RolVie2002": st.error("Mauvais code"); st.stop()
    if code=="RolVie2002":
        with st.form("pub",clear_on_submit=True):
            titre=st.text_input("Titre *")
            genre=st.selectbox("Genre",GENRES)
            annee=st.text_input("Année","2026")
            desc=st.text_area("Description")
            trailer=st.file_uploader("Bande Annonce Forte *",type=["mp4","mov","mkv"])
            film_complet=st.file_uploader("Film Complet",type=["mp4","mkv","mov"])
            affiche=st.file_uploader("Affiche",type=["jpg","png","jpeg","webp"])
            if st.form_submit_button("☁️ PUBLIER (reste à vie)",use_container_width=True):
                if titre and trailer and CLOUD_OK:
                    with st.spinner("Upload Cloudinary en cours... 1-2 min"):
                        trailer_url=upload_cloud(trailer,"congo_trailers")
                        film_url=upload_cloud(film_complet,"congo_films") if film_complet else None
                        image_url=upload_cloud(affiche,"congo_images") if affiche else None
                        new_f={"id":random.randint(100,99999),"titre":titre,"genre":genre,"annee":annee,"desc":desc,"trailer_url":trailer_url,"film_url":film_url,"image_url":image_url,"date":str(date.today())}
                        st.session_state.films.append(new_f); save_films()
                        st.success(f"✅ {titre} sur Cloudinary! Il ne va plus se supprimer!"); st.balloons()
                else: st.warning("Titre + Trailer + Cloudinary config obligatoire")
        for f in st.session_state.films[:]:
            if st.button(f"🗑️ Supprimer {f['titre']}",key=f"d_{f['id']}"):
                st.session_state.films=[x for x in st.session_state.films if x["id"]!=f["id"]]; save_films(); st.rerun()
else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    st.info("MTN 066778924 - 3500F Simple / 5000F Plus")
