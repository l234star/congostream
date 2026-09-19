import streamlit as st
import random, json, os
from datetime import datetime

FILMS_FILE = "films.json"
UPLOAD_DIR = "uploads"

# Crée les dossiers si besoin
os.makedirs(f"{UPLOAD_DIR}/trailers", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/films", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/images", exist_ok=True)

# === GESTION DES FILMS ===
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

# === UPLOAD CLOUD + LOCAL ===
def upload_cloud(file_obj, folder):
    if not file_obj:
        return None, 0
    # 1. Essaye Cloudinary si configuré
    try:
        if "CLOUDINARY_URL" in st.secrets or "cloudinary" in st.secrets:
            import cloudinary.uploader
            res = cloudinary.uploader.upload(file_obj, folder=f"congo_{folder}", resource_type="auto")
            return res.get("secure_url"), res.get("duration", 0)
    except:
        pass
    
    # 2. Fallback local (marche toujours)
    try:
        file_path = os.path.join(UPLOAD_DIR, folder, file_obj.name)
        with open(file_path, "wb") as out:
            out.write(file_obj.getbuffer())
        return file_path, 0
    except Exception as e:
        st.error(f"Erreur upload: {e}")
        return None, 0

# On tente d'importer l'ancien storage si il existe, sinon on utilise nos fonctions locales
try:
    from src.congostream.storage import upload_cloud as external_upload, save_films as external_save
    upload_cloud = external_upload
    save_films_original = external_save
    def save_films():
        try:
            external_save()
        except:
            with open(FILMS_FILE, "w", encoding="utf-8") as f:
                json.dump(st.session_state.films, f, ensure_ascii=False, indent=2)
except:
    try:
        from congostream.storage import upload_cloud as external_upload, save_films as external_save
        upload_cloud = external_upload
        def save_films():
            try:
                external_save()
            except:
                with open(FILMS_FILE, "w", encoding="utf-8") as f:
                    json.dump(st.session_state.films, f, ensure_ascii=False, indent=2)
    except:
        try:
            from storage import upload_cloud as external_upload, save_films as external_save
            upload_cloud = external_upload
            def save_films():
                try:
                    external_save()
                except:
                    with open(FILMS_FILE, "w", encoding="utf-8") as f:
                        json.dump(st.session_state.films, f, ensure_ascii=False, indent=2)
        except:
            pass # On garde nos fonctions locales

if "films" not in st.session_state:
    st.session_state.films = load_films()

# === INTERFACE ===
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
                        st.success("Publié! Le film apparaît maintenant!")
                        st.rerun()
                else:
                    st.warning("Ajoute au moins Titre + Trailer Boss!")

    with t2:
        st.subheader(f"{len(st.session_state.films)} Films publiés")
        for film in reversed(st.session_state.films):
            c1, c2 = st.columns([1, 3])
            with c1:
                if film.get("image_url"):
                    try:
                        st.image(film["image_url"], width=80)
                    except:
                        pass
            with c2:
                st.write(f"**{film['titre']}** - {film.get('timestamp','')}")
                if st.button("Supprimer", key=f"del_{film['id']}"):
                    st.session_state.films = [x for x in st.session_state.films if x["id"] != film["id"]]
                    save_films()
                    st.rerun()
            st.divider()

else:
    if password:
        st.error("Mauvais mot de passe")
    st.title("S'abonner")
    st.info("MTN 066778924 - 2000 FCFA / mois")
