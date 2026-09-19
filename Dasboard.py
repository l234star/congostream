import streamlit as st
from datetime import datetime
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
    except: return None

GENRES=["Tous","Action","Animation","Aventure","Biopic","Comedie","Documentaire","Drame","Horreur","Erotique","Espionnage","Fantastique","Guerre","Policier","Romance","Sci-Fi","Thriller"]

st.markdown("""
<style>
header{visibility:hidden!important;}
.stApp{background:#000!important;}
.block-container{padding-top:100px!important;}

/* HEADER NETFLIX - LOGO EN HAUT A GAUCHE DANS ZONE BLANCHE */
.netflix-header{
    position:fixed!important;
    top:0!important;
    left:0!important;
    right:0!important;
    height:52px!important;
    z-index:9999999!important;
    background:linear-gradient(to bottom, rgba(0,0,0,0.95), rgba(0,0,0,0.7))!important;
    display:flex!important;
    align-items:center!important;
    justify-content:space-between!important;
    padding:0 20px!important;
    border-bottom:1px solid rgba(255,255,255,0.1)!important;
}
.netflix-logo{
    color:#E50914!important;
    font-weight:900!important;
    font-size:26px!important;
    letter-spacing:2px!important;
    font-family:Arial Black!important;
}
.genre-bar{
    position:fixed!important;
    top:52px!important;
    left:0!important;
    right:0!important;
    z-index:9999998!important;
    background:#000!important;
    padding:8px 15px!important;
    display:flex!important;
    gap:8px!important;
    overflow-x:auto!important;
    white-space:nowrap!important;
    border-bottom:1px solid #222!important;
}
div[data-testid="stSegmentedControl"]{background:transparent!important;}
button[data-testid="stBaseButton-pills"]{background:rgba(255,255,255,0.15)!important;border:1px solid rgba(255,255,255,0.2)!important;border-radius:20px!important;color:white!important;}
button[data-testid="stBaseButton-pills"][data-active="true"]{background:#E50914!important;}
</style>
""", unsafe_allow_html=True)

# HEADER NETFLIX
st.markdown('<div class="netflix-header"><div class="netflix-logo">CONGOSTREAM</div><div style="color:white;">☰</div></div>', unsafe_allow_html=True)

DATA_FILE="congo_films_cloud.json"
if "films" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,"r") as f: st.session_state.films=json.load(f)
        except: st.session_state.films=[]
    else: st.session_state.films=[]
for k in ["selected_film","playing_film","menu_open","current_page","hero_index","genre_filter","edit_id"]:
    if k not in st.session_state:
        st.session_state[k] = None if k in ["selected_film","edit_id"] else False if k in ["playing_film","menu_open"] else "Accueil" if k=="current_page" else 0 if k=="hero_index" else "Tous"

def save_films():
    with open(DATA_FILE,"w") as f: json.dump(st.session_state.films,f,indent=2,default=str)

if st.session_state.current_page=="Accueil":
    st.markdown('<div class="genre-bar">', unsafe_allow_html=True)
    sel=st.pills("",GENRES,default=st.session_state.genre_filter,selection_mode="single",label_visibility="collapsed")
    if sel: st.session_state.genre_filter=sel
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("☰ Menu Navigation"):
    st.session_state.menu_open=not st.session_state.menu_open
if st.session_state.menu_open:
    choix=st.radio("Aller vers", ["Accueil","Espace Associe","S'abonner"], label_visibility="collapsed")
    st.session_state.current_page=choix
    if st.button("Fermer"):
        st.session_state.menu_open=False
        st.rerun()

menu=st.session_state.current_page

if menu=="Accueil":
    filtered=[f for f in st.session_state.films if st.session_state.genre_filter=="Tous" or f["genre"]==st.session_state.genre_filter]
    if filtered:
        hero=filtered[st.session_state.hero_index % len(filtered)]
        if hero.get("trailer_url"): st.video(hero["trailer_url"])
        elif hero.get("image_url"): st.image(hero["image_url"], use_container_width=True)
        if st.button("▶ LECTURE", type="primary", use_container_width=True):
            st.session_state.selected_film=hero["id"]; st.session_state.playing_film=True; st.rerun()
        if st.button("⏭ Film suivant"): st.session_state.hero_index+=1; st.rerun()
        st.markdown(f"### {hero['titre']}")

    for film in filtered:
        st.divider()
        if film.get("trailer_url"): st.video(film["trailer_url"])
        st.write(f"**{film['titre']}** - {film['genre']} - {film['annee']}")
        if st.button(f"Voir", key=f"v_{film['id']}"):
            st.session_state.selected_film=film["id"]; st.rerun()

elif menu=="Espace Associe":
    st.title("Espace Associe")
    code=st.text_input("Code", type="password")
    if code=="RolVie2002":
        t1,t2=st.tabs(["Publier","Gerer"])
        with t1:
            with st.form("pub", clear_on_submit=True):
                titre=st.text_input("Titre *")
                genre=st.selectbox("Genre", GENRES[1:])
                annee=st.text_input("Annee","2026")
                desc=st.text_area("Description")
                trailer=st.file_uploader("Bande Annonce *", type=["mp4","mov","mkv"])
                film_c=st.file_uploader("Film Complet", type=["mp4","mkv"])
                affiche=st.file_uploader("Pochette / Affiche", type=["jpg","png","webp"])
                if st.form_submit_button("PUBLIER", type="primary"):
                    if titre and trailer:
                        t_url=upload_cloud(trailer,"congo_trailers")
                        f_url=upload_cloud(film_c,"congo_films") if film_c else None
                        i_url=upload_cloud(affiche,"congo_images") if affiche else None
                        if t_url:
                            now=datetime.now()
                            st.session_state.films.append({"id":random.randint(1000,99999),"titre":titre,"genre":genre,"annee":annee,"desc":desc,"trailer_url":t_url,"film_url":f_url,"image_url":i_url,"timestamp":now.strftime("%d/%m/%Y à %H:%M:%S")})
                            save_films(); st.success("Publie!"); st.balloons()
        with t2:
            for film in reversed(st.session_state.films):
                st.write(f"**{film['titre']}** | {film.get('timestamp','')} | {film['genre']}")
                if film.get("image_url"): st.image(film["image_url"], width=90)
                if st.button("Supprimer", key=f"d_{film['id']}"):
                    st.session_state.films=[f for f in st.session_state.films if f["id"]!=film["id"]]; save_films(); st.rerun()

else:
    st.title("S'abonner")
    st.info("MTN 066778924")
