import streamlit as st
import random, json, os
from datetime import datetime

FILMS_FILE = "films.json"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/trailers", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/films", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/images", exist_ok=True)

def load_films():
    if os.path.exists(FILMS_FILE):
        try:
            with open(FILMS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_films():
    with open(FILMS_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.films, f, ensure_ascii=False, indent=2)

def upload_cloud(file_obj, folder):
    """Upload local - marche sans Cloudinary"""
    if not file_obj:
        return None, 0
    try:
        # Si Cloudinary est configuré dans Secrets, on l'utilise
        if "CLOUDINARY_URL" in st.secrets or "cloudinary" in st.secrets:
            import cloudinary.uploader
            res = cloudinary.uploader.upload(file_obj, folder=folder, resource_type="auto")
            return res.get("secure_url"), res.get("duration", 0)
    except:
        pass
    
    # Fallback: sauvegarde locale
    try:
        file_path = os.path.join(UPLOAD_DIR, folder, file_obj.name)
        with open(file_path, "wb") as out:
            out.write(file_obj.getbuffer())
        # On retourne le chemin local
        return file_path, 0
    except Exception as e:
        st.error(f"Erreur upload: {e}")
        return None, 0

if "films" not in st.session_state:
    st.session_state.films = load_films()

st.title("Dashboard CongoStream")
password = st.text_input("Mot de passe Admin", type="password")

if password == "congo2024" or password == "1234":
    t1, t2 = st.tabs(["Publier Film", "Gérer Films"])
    with t1:
        st.subheader("Publier un nouveau film")
        with st.form("form_film", clear_on_submit=True):
            titre = st.text_input("Titre du film *")
            genre = st.selectbox("Genre", ["Action", "Comédie", "Drame", "Documentaire", "Nollywood", "Autre"])
            annee = st.number_input("Année", 1900, 2030, 2024)
            desc = st.text_area("Description")
            trailer = st.file_uploader("Trailer * (obligatoire)", type=["mp4", "mov", "mkv"])
            film_c = st.file_uploader("Film complet (optionnel)", type=["mp4", "mov", "mkv"])
            affiche = st.file_uploader("Affiche (image)", type=["jpg", "png", "jpeg"])
            
            if st.form_submit_button("PUBLIER", type="primary"):
                if titre and trailer:
                    with st.spinner("Upload en cours Boss..."):
                        t_url, t_duree = upload_cloud(trailer, "trailers")
                        f_url, _ = upload_cloud(film_c, "films") if film_c else (None, 0)
                        i_url, _ = upload_cloud(affiche, "images") if affiche else (None, 0)
                    if t_url:
                        now = datetime.now()
                        st.session_state.films.append({
                            "id": random.randint(1000, 99999),
                            "titre": titre,
                            "duree": t_duree,
                            "genre": genre,
                            "annee": annee,
                            "desc": desc,
                            "trailer_url": t_url,
                            "film_url": f_url,
                            "image_url": i_url,
                            "timestamp": now.strftime("%d/%m/%Y a %H:%M:%S")
                        })
                        save_films()
                        st.balloons()
                        st.success("Publié avec upload Boss!")
                        st.rerun()
                else:
                    st.warning("Ajoute Titre + Trailer Boss!")

    with t2:
        st.subheader(f"{len(st.session_state.films)} Films publiés")
        for film in reversed(st.session_state.films):
            st.write(f"**{film['titre']}** - {film.get('timestamp','')}")
            if film.get("image_url") and os.path.exists(film["image_url"]):
                st.image(film["image_url"], width=80)
            elif film.get("image_url"):
                st.image(film["image_url"], width=80)
            if film.get("trailer_url"):
                if os.path.exists(film["trailer_url"]):
                    st.video(film["trailer_url"])
                else:
                    st.video(film["trailer_url"])
            if st.button("Supprimer", key=f"del_{film['id']}"):
                st.session_state.films = [x for x in st.session_state.films if x["id"] != film["id"]]
                save_films()
                st.rerun()
else:
    if password:
        st.error("Mauvais mot de passe")
    st.title("S'abonner")
    st.info("MTN 066778924 - 2000 FCFA / mois")
