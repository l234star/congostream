import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

# --- INTRO VERT JAUNE ROUGE + FOND AFRIQUE LIVE ---
if "intro_done" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:99999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 3.5s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;">
            <div style="flex:1;background:#009543;animation: slideUp 0.7s 0.1s both;"></div>
            <div style="flex:1;background:#FBDE4A;animation: slideUp 0.7s 0.4s both;"></div>
            <div style="flex:1;background:#DC241F;animation: slideUp 0.7s 0.7s both;"></div>
        </div>
        <h1 style="z-index:2;color:white;font-size:60px;font-weight:900;letter-spacing:5px;animation: zoomIn 0.8s 1.2s both;">CONGO<span style="color:#FBDE4A;">STREAM</span></h1>
    </div>
    <style>
    @keyframes slideUp { from {transform: translateY(100%);} to {transform: translateY(0%);} }
    @keyframes zoomIn { from {opacity:0;transform:scale(0.5);} to {opacity:1;transform:scale(1);} }
    @keyframes fadeOut { to {opacity:0;visibility:hidden;} }
    </style>
    """, unsafe_allow_html=True)
    st.session_state.intro_done = True

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top, #1a0a00 0%, #000 70%); color:white; }
.netflix-title { color:#E50914; font-weight:900; font-size:38px; text-shadow: 0 0 15px #E50914; }
.film-card { background: rgba(20,20,20,0.95); border-radius:12px; padding:10px; border:1px solid #333; }
.film-card:hover { border-color:#E50914; transform: translateY(-5px); transition:0.3s; }
.live-dot { width:10px; height:10px; background:#E50914; border-radius:50%; display:inline-block; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(229,9,20,0.7);} 70%{box-shadow:0 0 0 10px rgba(229,9,20,0);} 100%{box-shadow:0 0 0 0 rgba(229,9,20,0);} }
header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
if "films" not in st.session_state:
    st.session_state.films = [
        {"id":1, "titre":"Boruto Naruto Next", "categorie":"Série", "genre":"ANIMÉ", "annee":"2024", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "trailer":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "image":"https://image.tmdb.org/t/p/w500/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "type":"Premium"},
        {"id":2, "titre":"Amour à Brazzaville", "categorie":"Film", "genre":"ROMANTIQUE", "annee":"2024", "youtube":"https://www.youtube.com/watch?v=jNQXAC9IVRw", "trailer":"https://www.youtube.com/watch?v=jNQXAC9IVRw", "image":"https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "type":"Gratuit"},
    ]
if "accueil" not in st.session_state:
    st.session_state.accueil = {"titre":"Boruto X Naruto - Exclu Congo", "desc":"Le combat final en exclusivité sur CONGOSTREAM - 3500F / 2 mois", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k"}
if "abonnes" not in st.session_state:
    st.session_state.abonnes = [{"nom":"Test Client", "id_mtn":"MTN123", "debut":"2026-09-01", "fin":"2026-11-01", "statut":"Actif"}]

# --- HEADER ---
c1, c2, c3 = st.columns([2,2,1])
with c1: st.markdown('<div class="netflix-title">CONGOSTREAM <span class="live-dot"></span></div>', unsafe_allow_html=True)
with c2: search = st.text_input("", placeholder="Rechercher...", label_visibility="collapsed")
with c3: menu = st.selectbox("", ["Accueil", "Espace Associé", "S'abonner 3500F"], label_visibility="collapsed")

# --- ACCUEIL ---
if menu == "Accueil":
    a = st.session_state.accueil
    st.video(a["youtube"])
    st.markdown(f"## {a['titre']}")
    st.write(a["desc"])
    st.divider()
    
    col_f1, col_f2 = st.columns(2)
    with col_f1: cat_f = st.selectbox("CATEGORIE", ["TOUT", "Film", "Série", "Documentaire"])
    with col_f2: genre_f = st.selectbox("GENRE", ["TOUS", "ANIMÉ", "SUSPENSE", "ROMANTIQUE", "GUERRE", "JEUNESSE", "ACTION", "COMÉDIE"])
    
    films = st.session_state.films
    if cat_f != "TOUT": films = [f for f in films if f["categorie"] == cat_f]
    if genre_f != "TOUS": films = [f for f in films if f["genre"] == genre_f]
    if search: films = [f for f in films if search.lower() in f["titre"].lower()]
    
    cols = st.columns(4)
    for i, film in enumerate(films):
        with cols[i % 4]:
            st.markdown('<div class="film-card">', unsafe_allow_html=True)
            st.image(film["image"], use_container_width=True)
            st.markdown(f"**{film['titre']}**")
            st.caption(f"{film['genre']} | {film['categorie']} | {film['annee']}")
            if st.button("Bande annonce", key=f"b_{film['id']}"): st.video(film["trailer"])
            if st.button("Regarder", key=f"r_{film['id']}"): st.video(film["youtube"])
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")

# --- ESPACE ASSOCIE ---
elif menu == "Espace Associé":
    st.title("Espace Associé")
    st.caption("Directeur: Seph NTOUMOU | BOSS: Toi (Patron)")
    code = st.text_input("Code Directeur / Boss", type="password")
    if st.button("ENTREE", use_container_width=True):
        if code == "RolVie2002":
            st.session_state["admin"] = True
        else:
            st.error("Mauvais code")

    if st.session_state.get("admin"):
        st.success("Bienvenue Patron - Directeur Seph, vous pouvez gérer")
        t1, t2, t3, t4 = st.tabs(["Publier (Upload)", "Gerer Films", "Modifier Accueil", "Abonnements"])

        with t1:
            st.subheader("Publier nouveau contenu - Avec Upload")
            with st.form("pub_form", clear_on_submit=True):
                titre = st.text_input("Titre *")
                cA, cB = st.columns(2)
                with cA:
                    categorie = st.selectbox("Categorie", ["Film", "Série", "Documentaire"])
                    genre = st.selectbox("Genre", ["ANIMÉ", "SUSPENSE", "ROMANTIQUE", "GUERRE", "JEUNESSE", "ACTION", "COMÉDIE"])
                with cB:
                    annee = st.text_input("Annee", "2024")
                    type_ac = st.selectbox("Type", ["Gratuit", "Premium - 3500F"])
                
                st.markdown("**Bande annonce (obligatoire pour Film ET Série)**")
                trailer_link = st.text_input("Lien YouTube Bande Annonce *")
                trailer_upload = st.file_uploader("OU Upload Bande Annonce depuis dossier", type=["mp4", "mov", "avi"])
                
                st.markdown("**Film / Série complet**")
                film_link = st.text_input("Lien YouTube Film Complet")
                film_upload = st.file_uploader("OU Upload Film Complet depuis dossier", type=["mp4", "mov", "avi", "mkv"])
                
                st.markdown("**Pochette / Affiche**")
                image_link = st.text_input("Lien image pochette https://...")
                image_upload = st.file_uploader("OU Upload Pochette depuis dossier", type=["jpg", "png", "jpeg", "webp"])
                
                pub = st.form_submit_button("PUBLIER MAINTENANT", use_container_width=True)
                if pub:
                    if titre and (trailer_link or trailer_upload):
                        final_trailer = trailer_link if trailer_link else "upload_trailer"
                        final_film = film_link if film_link else "upload_film"
                        final_image = image_link if image_link else "https://via.placeholder.com/500x750/000000/E50914?text=CONGOSTREAM"
                        st.session_state.films.append({"id": random.randint(100,9999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee, "youtube":final_film, "trailer":final_trailer, "image":final_image, "type":type_ac})
                        st.success(f"{titre} publie !")
                        st.balloons()
                    else:
                        st.warning("Titre + Bande annonce obligatoire")

        with t2:
            st.subheader("Gerer - Changer pochette et bande annonce")
            for film in st.session_state.films:
                with st.expander(f"{film['titre']} - {film['genre']}"):
                    col1, col2 = st.columns([1,2])
                    with col1: st.image(film["image"], width=150)
                    with col2:
                        nt = st.text_input("Titre", film["titre"], key=f"tit{film['id']}")
                        ni = st.text_input("Lien pochette", film["image"], key=f"img{film['id']}")
                        ntr = st.text_input("Lien bande annonce", film["trailer"], key=f"tra{film['id']}")
                        ny = st.text_input("Lien film complet", film["youtube"], key=f"yt{film['id']}")
                        up_img = st.file_uploader("Nouvelle pochette upload", type=["jpg","png"], key=f"upimg{film['id']}")
                        up_tr = st.file_uploader("Nouvelle bande annonce upload", type=["mp4","mov"], key=f"uptr{film['id']}")
                        if st.button("Sauver", key=f"sv{film['id']}"):
                            film["titre"]=nt; film["image"]=ni; film["trailer"]=ntr; film["youtube"]=ny
                            st.success("Sauve"); st.rerun()
                        if st.button("Supprimer", key=f"del{film['id']}"):
                            st.session_state.films = [f for f in st.session_state.films if f["id"] != film["id"]]
                            st.rerun()

        with t3:
            st.subheader("Modifier Accueil")
            acc = st.session_state.accueil
            acc["titre"] = st.text_input("Titre Accueil", acc["titre"])
            acc["desc"] = st.text_area("Description", acc["desc"])
            acc["youtube"] = st.text_input("Youtube Accueil", acc["youtube"])
            if st.button("Sauver Accueil"): st.success("Accueil modifie")

        with t4:
            st.subheader("Abonnements Actifs / Expires")
            actifs = [a for a in st.session_state.abonnes if a["statut"]=="Actif"]
            expires = [a for a in st.session_state.abonnes if a["statut"]=="Expire" or a["statut"]=="Expiré"]
            colA, colB = st.columns(2)
            with colA:
                st.markdown(f"**Actifs: {len(actifs)}**")
                for ab in actifs:
                    st.success(f"{ab['nom']} - {ab['id_mtn']} - Fin {ab['fin']}")
            with colB:
                st.markdown(f"**Expires: {len(expires)}**")
                for ab in expires:
                    st.error(f"{ab['nom']} - {ab['id_mtn']}")

else:
    st.markdown('<h1 style="color:#E50914;">3500F / 2 MOIS - PREMIUM</h1>', unsafe_allow_html=True)
    st.info("MTN MoMo: 066778924 - Entre ton nom et ID apres paiement")
    with st.form("ab_form"):
        nom = st.text_input("Nom")
        idm = st.text_input("ID MTN")
        if st.form_submit_button("Activer"):
            debut = datetime.now().strftime("%Y-%m-%d")
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "debut":debut, "fin":fin, "statut":"Actif"})
            st.success(f"Merci {nom}, actif jusquau {fin}")
