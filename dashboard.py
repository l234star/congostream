import streamlit as st
from datetime import datetime, timedelta, date
import random, os

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

GENRES_COMPLETS = ["Action", "Animation", "Aventure", "Biopic / Biographie", "Comédie", "Documentaire", "Drame", "Épouvante-Horreur", "Erotique", "Espionnage", "Fantastique", "Fantasy", "Film musical", "Guerre", "Historique", "Policier", "Romance", "Science-fiction", "Thriller", "Western"]

if "intro_done_v16" not in st.session_state:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;width:100%;height:100vh;z-index:9999999;background:#000;display:flex;align-items:center;justify-content:center;animation: fadeOut 1s ease 3.5s forwards;">
        <div style="display:flex;width:100%;height:100%;position:absolute;"><div style="flex:1;background:#009543;"></div><div style="flex:1;background:#FBDE4A;"></div><div style="flex:1;background:#DC241F;"></div></div>
        <h1 style="z-index:10;color:white;font-size:58px;font-weight:900;">CONGOSTREAM</h1>
    </div>
    <style>@keyframes fadeOut{to{opacity:0;visibility:hidden;}}</style>
    """, unsafe_allow_html=True)
    st.session_state.intro_done_v16 = True

st.markdown("""
<style>
.stApp { background:#000; color:white; }
.film-card { background:#111; border-radius:8px; overflow:hidden; border:1px solid #222; cursor:pointer; }
.film-card:hover { border-color:#E50914; transform:translateY(-4px); transition:0.2s; }
.film-title { padding:8px; font-weight:700; font-size:14px; text-align:center; background:#181818; }
.lecture-coin { position:fixed; top:90px; right:30px; z-index:999; background:#E50914; color:white; padding:12px 25px; border-radius:30px; font-weight:900; box-shadow:0 4px 15px rgba(229,9,20,0.6); }
header{visibility:hidden;}
.stButton>button { border-radius:20px; font-weight:900; }
</style>
""", unsafe_allow_html=True)

os.makedirs("videos", exist_ok=True); os.makedirs("trailers", exist_ok=True); os.makedirs("images", exist_ok=True)

if "films" not in st.session_state: st.session_state.films = []
if "abonnes" not in st.session_state: st.session_state.abonnes = []
if "selected_film" not in st.session_state: st.session_state.selected_film = None
if "user_tier" not in st.session_state: st.session_state.user_tier = "Gratuit"
if "playing_film" not in st.session_state: st.session_state.playing_film = False

def save_file(f, folder):
    if f:
        p = os.path.join(folder, f.name)
        with open(p, "wb") as out: out.write(f.getbuffer())
        return p
    return None

c1, c2 = st.columns([5,1])
with c1: st.markdown('<div style="color:#E50914; font-weight:900; font-size:32px;">CONGOSTREAM</div>', unsafe_allow_html=True)
with c2: menu = st.selectbox("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed")

# ============ DETAIL FILM - COMME TU VEUX ============
if st.session_state.selected_film and menu == "Accueil":
    film = next((f for f in st.session_state.films if f["id"] == st.session_state.selected_film), None)
    if film:
        col_back, col_lecture = st.columns([3,1])
        with col_back:
            if st.button("⬅️ Retour aux films"): 
                st.session_state.selected_film=None
                st.session_state.playing_film=False
                st.rerun()
        with col_lecture:
            # BOUTON LECTURE AU COIN BIEN VISIBLE MAIS PAS GENANT
            if st.button("▶️ LECTURE", key="lecture_coin", use_container_width=True):
                if "Simple" in st.session_state.user_tier or "Plus" in st.session_state.user_tier:
                    # Vérif 4K
                    if film.get("qualite")=="4K" and "Plus" not in st.session_state.user_tier:
                        st.warning("🔒 4K réservé PLUS 5000F")
                    else:
                        st.session_state.playing_film = True
                else:
                    st.error("🔒 Abonnement requis! Va dans S'abonner - Bande annonce gratuite seulement")

        # TITRE
        st.markdown(f"<h2 style='margin:0;'>{film['titre']}</h2><p style='color:#aaa;'>{film['genre']} • {film['categorie']} • {film['annee']} • {film.get('qualite','HD')}</p>", unsafe_allow_html=True)

        # SI LECTURE CLIQUEE ET ABONNE -> JOUE LE FILM
        if st.session_state.playing_film:
            st.markdown("### 🎬 Film complet")
            if film.get("film_path") and os.path.exists(film["film_path"]):
                st.video(film["film_path"])
            else:
                st.error("Film complet pas encore uploadé par le Boss")
            if st.button("⏸️ Revoir bande annonce"):
                st.session_state.playing_film=False
                st.rerun()
        else:
            # SINON BANDE ANNONCE JOUE AUTOMATIQUEMENT QUAND ON CLIQUE SUR LE FILM
            st.markdown("### 🎬 Bande annonce (Gratuite - pas obligé de finir)")
            if film.get("trailer_path") and os.path.exists(film["trailer_path"]):
                st.video(film["trailer_path"])
                st.caption("Bande annonce gratuite. Clique sur LECTURE en haut à droite pour le film complet (abonnement requis)")
            else:
                st.warning("Bande annonce non disponible")
            if film.get("is_annonce") and film.get("date_sortie"):
                st.info(f"🔔 Sortie prévue le {film['date_sortie'].strftime('%d/%m/%Y')}")

# ============ ACCUEIL - IMAGE DANS CADRE + TITRE EN BAS ============
elif menu == "Accueil":
    tier = st.selectbox("👤 Mon forfait:", ["Gratuit (Bande annonce seulement)", "Simple - 3500F", "Plus - 5000F"], label_visibility="collapsed")
    st.session_state.user_tier = tier

    if not st.session_state.films:
        st.info("Aucun film. Va dans Espace Associé > Publier pour upload tes vidéos")
    else:
        # FILTRE GENRE COMME NETFLIX
        genre_filter = st.selectbox("🎭 Filtrer par genre", ["TOUS"] + GENRES_COMPLETS)
        films = st.session_state.films
        if genre_filter != "TOUS": films = [f for f in films if f["genre"] == genre_filter]

        st.markdown(f"### 🎬 {genre_filter} - {len(films)} films")

        cols = st.columns(4)
        for i, film in enumerate(films):
            with cols[i % 4]:
                # IMAGE DANS CADRE + TITRE EN BAS
                st.markdown('<div class="film-card">', unsafe_allow_html=True)
                if film.get("image_path") and os.path.exists(film["image_path"]):
                    st.image(film["image_path"], use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/400x600/111/E50914?text=CONGOSTREAM", use_container_width=True)
                st.markdown(f"<div class='film-title'>{film['titre']}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # CLIC SUR LE FILM = BANDE ANNONCE
                if st.button(f"Voir {film['titre'][:15]}", key=f"voir_{film['id']}", use_container_width=True):
                    st.session_state.selected_film = film["id"]
                    st.session_state.playing_film = False
                    st.rerun()

elif menu == "Espace Associé":
    st.title("Espace Associé - BOSS")
    if not st.session_state.get("admin"):
        code = st.text_input("Code", type="password", placeholder="RolVie2002")
        if st.button("🔓 ENTRÉE", use_container_width=True):
            if code == "RolVie2002": st.session_state["admin"]=True; st.rerun()
            else: st.error("Mauvais code")
        st.stop()
    if st.button("Déconnexion"): st.session_state["admin"]=False; st.rerun()
    t1, t2 = st.tabs(["📤 Publier", "🗑️ Supprimer"])
    with t1:
        with st.form("pub_v16", clear_on_submit=True):
            titre = st.text_input("Titre *")
            is_annonce = st.checkbox("🔔 Bande annonce d'annonce (date de sortie)")
            cA, cB = st.columns(2)
            with cA:
                categorie = st.selectbox("Catégorie", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre *", GENRES_COMPLETS)
            with cB:
                annee = st.text_input("Année", "2026")
                qualite = st.selectbox("Qualité", ["HD - Simple", "4K - Plus"])
                date_sortie = st.date_input("📅 Date sortie", value=date.today()+timedelta(days=7)) if is_annonce else None
            desc = st.text_area("Description")
            trailer_file = st.file_uploader("Upload Bande Annonce * (gratuit)", type=["mp4","mov","mkv","avi"])
            film_file = st.file_uploader("Upload Film Complet (payant - sera lu avec LECTURE)", type=["mp4","mkv","mov","avi"]) if not is_annonce else None
            image_file = st.file_uploader("Upload Affiche (image dans cadre)", type=["jpg","png","jpeg","webp"])
            if st.form_submit_button("🔓 ENTRÉE - PUBLIER", use_container_width=True):
                if titre and trailer_file:
                    tp = save_file(trailer_file, "trailers")
                    fp = save_file(film_file, "videos") if film_file else None
                    ip = save_file(image_file, "images") if image_file else None
                    st.session_state.films.append({"id": random.randint(100,99999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee, "desc":desc, "trailer_path":tp, "film_path":fp, "image_path":ip, "qualite":"4K" if "4K" in qualite else "HD", "is_annonce":is_annonce, "date_sortie":date_sortie})
                    st.success("Publié!"); st.balloons()
                else: st.warning("Titre + Bande annonce obligatoire")
    with t2:
        for film in st.session_state.films[:]:
            col1, col2 = st.columns([4,1])
            with col1: st.write(f"**{film['titre']}** - {film['genre']} {'🔔 ANNONCE' if film.get('is_annonce') else ''}")
            with col2:
                if st.button("🗑️", key=f"del_{film['id']}"):
                    for p in [film.get("trailer_path"), film.get("film_path"), film.get("image_path")]:
                        if p and os.path.exists(p):
                            try: os.remove(p)
                            except: pass
                    st.session_state.films = [f for f in st.session_state.films if f["id"]!= film["id"]]; st.rerun()
else:
    st.markdown('<h1 style="color:#E50914;">Abonnements</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.info("**SIMPLE 3500F**\n✅ HD\n❌ Pas 4K")
    with c2: st.success("**PLUS 5000F**\n✅ 4K\n✅ Demande\n✅ Assistance 24h/24")
    with st.form("ab_v16"):
        nom = st.text_input("Nom"); idm = st.text_input("ID MTN 066778924")
        type_c = st.selectbox("Forfait", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "fin":fin, "type":type_c})
            st.success(f"{nom} actif jusqu'au {fin} - Maintenant LECTURE va marcher!")
