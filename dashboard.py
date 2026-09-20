import streamlit as st
import os, json, random
from datetime import datetime
import cloudinary, cloudinary.uploader

st.set_page_config(page_title="CongoStream", layout="wide")
CODE_ADMIN = "JOKSAN2026"
NUMERO = "066778924"

# Config ultra simple - juste le cloud_name, pas de clé
cloudinary.config(cloud_name="xwvmq9dj")
OK = True

FILMS_FILE="films.json"; TRANSAC_FILE="transactions.json"
def charger(nom):
    if os.path.exists(nom):
        try:
            with open(nom,"r",encoding="utf-8") as f: return json.load(f)
        except: return []
    return []
def sauver(nom,data):
    with open(nom,"w",encoding="utf-8") as f: json.dump(data,f,indent=2,ensure_ascii=False)

def upload(file, folder):
    if not file: return ""
    try:
        # PRESET ml_default existe déjà par défaut en unsigned - ça marche même avec ton erreur
        r = cloudinary.uploader.unsigned_upload(file, "ml_default", folder=folder, resource_type="auto")
        return r.get("secure_url","")
    except Exception as e:
        st.error(f"Erreur upload: {e}")
        return ""

if "films" not in st.session_state: st.session_state.films=charger(FILMS_FILE)
if "trans" not in st.session_state: st.session_state.trans=charger(TRANSAC_FILE)
if "editing" not in st.session_state: st.session_state.editing=None
if "mes_acces" not in st.session_state: st.session_state.mes_acces=[]

films=st.session_state.films
st.markdown('<div style="background:#000;padding:15px;border-radius:10px;"><span style="color:#E50914;font-size:32px;font-weight:900;">CONGOSTREAM</span> <span style="color:white;margin-left:15px;">By.Mr_Joksan</span></div>', unsafe_allow_html=True)
tab1,tab2,tab3=st.tabs(["🏠 ACCUEIL","➕ PUBLIER (Code)","⚙️ GÉRER (Code)"])

with tab1:
    st.info(f"Gratuit = direct | Payant = {NUMERO} + ID")
    if not films: st.warning("Aucun film - va publier")
    else:
        cols=st.columns(3)
        for i,film in enumerate(reversed(films)):
            with cols[i%3]:
                with st.container(border=True):
                    if film.get("image_url"): st.image(film["image_url"],use_container_width=True)
                    st.write(f"**{film['titre']}**")
                    st.caption(f"{film.get('genre','')} | {film.get('paiement','Gratuit')}")
                    ba = film.get("bande_annonce_url") or film.get("trailer_url")
                    if ba:
                        st.video(ba)
                    if film.get("paiement")=="Gratuit":
                        vp = film.get("film_url") or film.get("video_url")
                        if vp and vp!=ba: st.video(vp)

with tab2:
    code=st.text_input("Code admin",type="password",key="pub")
    if code!=CODE_ADMIN: st.warning("Code: JOKSAN2026")
    else:
        with st.form("add",clear_on_submit=True):
            titre=st.text_input("Titre *")
            genre=st.selectbox("Genre",["Action","Congolais","Nollywood","Africain"])
            paiement=st.selectbox("Paiement",["Gratuit","Location 500 FCFA","Achat 2000 FCFA","MTN Money"])
            desc=st.text_area("Description")
            a,b,c=st.columns(3)
            with a: img=st.file_uploader("Affiche",type=["jpg","png","webp"])
            with b: ba=st.file_uploader("Bande Annonce SEULE - ça marche!",type=["mp4","mov"])
            with c: film_f=st.file_uploader("Film complet (optionnel)",type=["mp4","mkv"])
            if st.form_submit_button("🚀 Publier"):
                if titre:
                    with st.spinner("Upload en cours..."):
                        u1=upload(img,"congostream/affiches"); u2=upload(ba,"congostream/ba"); u3=upload(film_f,"congostream/films")
                        video_finale = u3 if u3 else u2
                        if not video_finale and not u1:
                            st.error("Upload a échoué - réessaye avec fichier plus petit < 50MB")
                        else:
                            st.session_state.films.append({"id":random.randint(1000,99999),"titre":titre,"genre":genre,"paiement":paiement,"desc":desc,"image_url":u1,"bande_annonce_url":u2,"trailer_url":u2,"film_url":u3,"video_url":video_finale})
                            sauver(FILMS_FILE,st.session_state.films); st.success(f"{titre} publié! Va dans ACCUEIL"); st.balloons()

with tab3:
    code2=st.text_input("Code admin",type="password",key="ger")
    if code2==CODE_ADMIN:
        for film in reversed(films):
            with st.expander(f"{film['titre']}"):
                if st.button("Supprimer",key=f"del_{film['id']}"): st.session_state.films=[x for x in films if x['id']!=film['id']]; sauver(FILMS_FILE,st.session_state.films); st.rerun()
