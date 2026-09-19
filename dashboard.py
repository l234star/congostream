import streamlit as st
import random
from datetime import datetime
try:
    from src.congostream.storage import upload_cloud, save_films
except:
    try:
        from congostream.storage import upload_cloud, save_films
    except:
        from storage import upload_cloud, save_films

if "films" not in st.session_state:
    st.session_state.films = []

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
                    t_url, t_duree = upload_cloud(trailer, "congo_trailers")
                    f_url, _ = upload_cloud(film_c, "congo_films") if film_c else (None, 0)
                    i_url, _ = upload_cloud(affiche, "congo_images") if affiche else (None, 0)
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
                        st.success("Publié!")
                        st.rerun()
                else:
                    st.warning("Ajoute au moins Titre + Trailer Boss!")

    with t2:
        st.subheader("Films publiés")
        for film in reversed(st.session_state.films):
            col1, col2 = st.columns([1, 3])
            with col1:
                if film.get("image_url"):
                    st.image(film["image_url"], width=80)
            with col2:
                st.write(f"**{film['titre']}** - {film.get('timestamp','')}")
                if st.button("Supprimer", key=f"del_{film['id']}"):
                    st.session_state.films = [x for x in st.session_state.films if x["id"] != film["id"]]
                    save_films()
                    st.rerun()

else:
    st.title("S'abonner")
    st.info("MTN 066778924 - 2000 FCFA / mois")
    st.write("Contacte l'admin pour avoir le mot de passe")
