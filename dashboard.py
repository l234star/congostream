import streamlit as st
import os, json, random, requests
from datetime import datetime

st.set_page_config(page_title="CongoStream", layout="wide")
CODE_ADMIN = "JOKSAN2026"
NUMERO = "066778924"

def upload(file, folder):
    if not file: return ""
    try:
        # Upload direct sans API KEY, juste avec preset unsigned
        url = "https://api.cloudinary.com/v1_1/xwvmq9dj/auto/upload"
        files = {"file": (file.name, file.getvalue(), file.type)}
        data = {"upload_preset": "congostream", "folder": folder}
        r = requests.post(url, data=data, files=files, timeout=60)
        if r.status_code == 200:
            return r.json().get("secure_url","")
        else:
            st.error(f"Cloudinary dit: {r.text[:200]}")
            return ""
    except Exception as e:
        st.error(f"Erreur: {e}")
        return ""

FILMS_FILE="films.json"; TRANSAC_FILE="transactions.json"
def charger(nom):
    if os.path.exists(nom):
        try:
            with open(nom,"r",encoding="utf-8") as f: return json.load(f)
        except: return []
    return []
def sauver(nom,data):
    with open(nom,"w",encoding="utf-8") as f: json.dump(data,f,indent=2,ensure_ascii=False)

if "films" not in st.session_state: st.session_state.films=charger(FILMS_FILE)
if "trans" not in st.session_state: st.session_state.trans=charger(TRANSAC_FILE)
if "mes_acces" not in st.session_state: st.session_state.mes_acces=[]

films=st.session_state.films
st.markdown('<div style="background:#000;padding:15px;border-radius:10px;"><span style="color:#E50914;font-size:32px;font-weight:900;">CONGOSTREAM</span></div>', unsafe_allow_html=True)
tab1,tab2,tab3=st.tabs(["🏠 ACCUEIL","➕ PUBLIER","⚙️ GÉRER"])

with tab1:
    if not films: st.warning("Aucun film")
    else:
        cols=st.columns(3)
        for i,film in enumerate(reversed(films)):
            with cols[i%3]:
                with st.container(border=True):
                    if film.get("image_url"): st.image(film["image_url"],use_container_width=True)
                    st.write(f"**{film['titre']}**")
                    ba = film.get("bande_annonce_url")
                    if ba: st.video(ba)
                    if film.get("paiement")=="Gratuit":
                        vp = film.get("film_url")
                        if vp and vp!=ba: st.video(vp)

with tab2:
    code=st.text_input("Code admin",type="password")
    if code==CODE_ADMIN:
        with st.form("add",clear_on_submit=True):
            titre=st.text_input("Titre *")
            paiement=st.selectbox("Paiement",["Gratuit","Location 500 FCFA","Achat 2000 FCFA"])
            a,b,c=st.columns(3)
            with a: img=st.file_uploader("Affiche",type=["jpg","png","webp"])
            with b: ba=st.file_uploader("Bande Annonce SEULE",type=["mp4","mov"])
            with c: film_f=st.file_uploader("Film complet (optionnel)",type=["mp4","mkv"])
            if st.form_submit_button("🚀 Publier"):
                with st.spinner("Upload... 30 sec"):
                    u1=upload(img,"congostream/affiches"); u2=upload(ba,"congostream/ba"); u3=upload(film_f,"congostream/films")
                    video_finale = u3 if u3 else u2
                    st.session_state.films.append({"id":random.randint(1000,99999),"titre":titre,"paiement":paiement,"image_url":u1,"bande_annonce_url":u2,"film_url":u3,"video_url":video_finale})
                    sauver(FILMS_FILE,st.session_state.films); st.success("Publié! Va dans ACCUEIL"); st.balloons()

with tab3:
    if st.text_input("Code Gérer",type="password",key="g")==CODE_ADMIN:
        for f in films:
            st.write(f"{f['titre']} - {f['paiement']}")
