import streamlit as st
from datetime import datetime
import random, os, json, tempfile
import cloudinary
import cloudinary.uploader

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")
CLOUD_OK=False
try:
    cloudinary.config(cloud_name=st.secrets["cloudinary"]["cloud_name"],api_key=st.secrets["cloudinary"]["api_key"],api_secret=st.secrets["cloudinary"]["api_secret"],secure=True)
    CLOUD_OK=True
except: CLOUD_OK=False

def upload_cloud(f,folder):
    if not f or not CLOUD_OK: return None
    try:
        s=os.path.splitext(f.name)[1]
        with tempfile.NamedTemporaryFile(delete=False,suffix=s) as t:
            t.write(f.getvalue())
            p=t.name
        r=cloudinary.uploader.upload(p,resource_type="auto",folder=folder,chunk_size=6000000)
        os.remove(p)
        return r.get("secure_url")
    except: return None

GENRES=["Tous","Action","Animation","Aventure","Biopic","Comedie","Documentaire","Drame","Horreur","Erotique","Espionnage","Fantastique","Guerre","Policier","Romance","Sci-Fi","Thriller"]

st.markdown("""
<style>
header{visibility:hidden!important;}
.stApp{background:#000!important;}
.block-container{padding-top:95px!important;}
/* LOGO NETFLIX A GAUCHE */
.netflix-top{
    position:fixed!important;
    top:0!important; left:0!important; right:0!important;
    height:50px!important;
    background:#000!important;
    z-index:99999999!important;
    display:flex!important;
    align-items:center!important;
    padding-left:15px!important;
    border-bottom:1px solid #222!important;
}
.netflix-top h1{
    color:#E50914!important;
    font-size:24px!important;
    font-weight:900!important;
    letter-spacing:2px!important;
    margin:0!important;
}
.genre-fixed{
    position:fixed!important;
    top:50px!important; left:0!important; right:0!important;
    background:#000!important;
    z-index:9999998!important;
    padding:8px 12px!important;
    display:flex!important; gap:6px!important; overflow-x:auto!important; white-space:nowrap!important;
}
</style>
<div class="netflix-top"><h1>CONGOSTREAM</h1></div>
""", unsafe_allow_html=True)

DATA_FILE="congo_films_cloud.json"
if "films" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,"r") as f: st.session_state.films=json.load(f)
        except: st.session_state.films=[]
    else: st.session_state.films=[]
for k in ["selected_film","playing_film","menu_open","current_page","hero_index","genre_filter","edit_id"]:
    if k not in st.session_state:
        st.session_state[k]=None if k in ["selected_film","edit_id"] else False if k in ["playing_film","menu_open"] else "Accueil" if k=="current_page" else 0 if k=="hero_index" else "Tous"

def save_films():
    with open(DATA_FILE,"w") as f: json.dump(st.session_state.films,f,indent=2,default=str)

# MENU
if st.session_state.current_page=="Accueil":
    st.markdown('<div class="genre-fixed">', unsafe_allow_html=True)
    s=st.pills("",GENRES,default=st.session_state.genre_filter,selection_mode="single",label_visibility="collapsed")
    if s: st.session_state.genre_filter=s
    st.markdown('</div>', unsafe_allow_html=True)

c1,c2=st.columns([1,5])
with c1:
    if st.button("☰"):
        st.session_state.menu_open=not st.session_state.menu_open
if st.session_state.menu_open:
    ch=st.radio("",["Accueil","Espace Associe","S'abonner"],label_visibility="collapsed")
    st.session_state.current_page=ch
    if st.button("Fermer"): st.session_state.menu_open=False; st.rerun()

menu=st.session_state.current_page
menu=="Accueil":
    filtered=[f for f in st.session_state.films if st.session_state.genre_filter=="Tous" or f["genre"]==st.session_state.genre_filter]
    if filtered:
        hero=filtered[st.session_state.hero_index % len(filtered)]
        
        # 1 SEULE FENETRE PRINCIPALE
        if hero.get("trailer_url"): 
            st.video(hero["trailer_url"])
        st.write(f"**{hero['titre']}**")
        
        c1,c2=st.columns(2)
        with c1:
            if st.button("◀ Précédent"):
                st.session_state.hero_index -= 1
                st.rerun()
        with c2:
            if st.button("Suivant ▶"):
                st.session_state.hero_index += 1
                st.rerun()
        
        st.divider()
        st.subheader("Tous les films")
        
        # CARREAUX EN BAS
        cols = st.columns(4)
        for idx, f in enumerate(filtered):
            with cols[idx % 4]:
                if f.get("image_url"):
                    st.image(f["image_url"], use_container_width=True)
                st.write(f"**{f['titre']}**")
                if st.button("Voir", key=f"tile_{f['id']}", use_container_width=True):
                    st.session_state.hero_index = idx
                    st.rerun()
elif menu=="Espace Associe":
    st.title("Espace Associe")
    code=st.text_input("Code",type="password")
    if code=="RolVie2002":
        t1,t2=st.tabs(["Publier","Gerer"])
        with t1:
            with st.form("pub",clear_on_submit=True):
                titre=st.text_input("Titre *")
                genre=st.selectbox("Genre",GENRES[1:])
                annee=st.text_input("Annee","2026")
                desc=st.text_area("Description")
                trailer=st.file_uploader("Bande Annonce *",type=["mp4","mov"])
                film_c=st.file_uploader("Film Complet",type=["mp4"])
                affiche=st.file_uploader("Pochette",type=["jpg","png","webp"])
                if st.form_submit_button("PUBLIER",type="primary"):
                    if titre and trailer:
                        t_url=upload_cloud(trailer,"congo_trailers")
                        f_url=upload_cloud(film_c,"congo_films") if film_c else None
                        i_url=upload_cloud(affiche,"congo_images") if affiche else None
                        if t_url:
                            now=datetime.now()
                            st.session_state.films.append({"id":random.randint(1000,99999),"titre":titre,"genre":genre,"annee":annee,"desc":desc,"trailer_url":t_url,"film_url":f_url,"image_url":i_url,"timestamp":now.strftime("%d/%m/%Y à %H:%M:%S")})
                            save_films(); st.balloons(); st.success("Publie!")
        with t2:
            for film in reversed(st.session_state.films):
                st.write(f"{film['titre']} - {film.get('timestamp','')}")
                if film.get("image_url"): st.image(film["image_url"],width=80)
                if st.button("Supprimer",key=f"del_{film['id']}"): st.session_state.films=[x for x in st.session_state.films if x["id"]!=film["id"]]; save_films(); st.rerun()
else:
    st.title("S'abonner")
    st.info("MTN 066778924")
