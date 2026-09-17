import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

# INTRO VERT JAUNE ROUGE
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
.netflix-title { color:#E50914; font-weight:900; font-size:38px; }
.film-card { background: rgba(20,20,20,0.95); border-radius:12px; padding:10px; border:1px solid #333; }
.film-card:hover { border-color:#E50914; transform: translateY(-5px); transition:0.3s; }
.badge-4k { background: gold; color:black; padding:2px 6px; border-radius:4px; font-weight:900; font-size:12px; }
.badge-plus { background: #E50914; color:white; padding:2px 6px; border-radius:4px; font-size:11px; }
.live-dot { width:10px; height:10px; background:#E50914; border-radius:50%; display:inline-block; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(229,9,20,0.7);} 70%{box-shadow:0 0 0 10px rgba(229,9,20,0);} 100%{box-shadow:0 0 0 0 rgba(229,9,20,0);} }
header{visibility:hidden;}
.stButton>button { background:#E50914; color:white; font-weight:bold; border-radius:6px; width:100%; }
</style>
""", unsafe_allow_html=True)

if "films" not in st.session_state:
    st.session_state.films = [
        {"id":1, "titre":"Boruto Naruto Next", "categorie":"Série", "genre":"ANIMÉ", "annee":"2024", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "trailer":"https://www.youtube.com/watch?v=Qp3b-Rhse9k", "image":"https://image.tmdb.org/t/p/w500/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "type":"Premium", "qualite":"4K"},
        {"id":2, "titre":"Amour à Brazzaville", "categorie":"Film", "genre":"ROMANTIQUE", "annee":"2024", "youtube":"https://www.youtube.com/watch?v=jNQXAC9IVRw", "trailer":"https://www.youtube.com/watch?v=jNQXAC9IVRw", "image":"https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "type":"Simple", "qualite":"HD"},
        {"id":3, "titre":"Guerre du Congo - Doc", "categorie":"Documentaire", "genre":"GUERRE", "annee":"2023", "youtube":"https://www.youtube.com/watch?v=9bZkp7q19f0", "trailer":"https://www.youtube.com/watch?v=9bZkp7q19f0", "image":"https://image.tmdb.org/t/p/w500/7RyHsO4yDXtBv1zUU3mTpHeQd.jpg", "type":"Plus", "qualite":"4K"},
    ]
if "accueil" not in st.session_state:
    st.session_state.accueil = {"titre":"Exclu Congo - 4K pour les PLUS", "desc":"Le Netflix du Congo", "youtube":"https://www.youtube.com/watch?v=Qp3b-Rhse9k"}
if "abonnes" not in st.session_state:
    st.session_state.abonnes = []
if "user_tier" not in st.session_state:
    st.session_state.user_tier = "Gratuit"

# HEADER
c1, c2, c3 = st.columns([2,2,1])
with c1: st.markdown('<div class="netflix-title">CONGOSTREAM <span class="live-dot"></span></div>', unsafe_allow_html=True)
with c2: search = st.text_input("", placeholder="Rechercher...", label_visibility="collapsed", key="search_main")
with c3: menu = st.selectbox("", ["Accueil", "Espace Associé", "S'abonner"], label_visibility="collapsed", key="menu_main")

# ACCUEIL AVEC 2 INTERFACES
if menu == "Accueil":
    a = st.session_state.accueil
    st.video(a["youtube"])

    # SELECTEUR DE FORFAIT POUR VOIR LA DIFFERENCE
    tier = st.selectbox("👤 Mon forfait actuel:", ["Gratuit", "Simple - 3500F", "Plus - 5000F"], key="tier_selector")
    if "Plus" in tier: st.session_state.user_tier = "Plus"
    elif "Simple" in tier: st.session_state.user_tier = "Simple"
    else: st.session_state.user_tier = "Gratuit"

    if st.session_state.user_tier == "Plus":
        st.markdown("""
        <div style="background:linear-gradient(90deg, gold, #E50914);padding:15px;border-radius:10px;color:black;font-weight:bold;">
        👑 MODE PLUS ACTIVÉ - 4K | Film à la demande | Réservation 24h | Assistance 24h/24
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.form("demande_film"):
                st.markdown("**🎬 Film à la demande**")
                demande = st.text_input("Quel film veux-tu?")
                if st.form_submit_button("🔓 ENTRÉE - Demander"):
                    st.success(f"Demande '{demande}' envoyée au Boss! Disponible sous 24h")
        with col2:
            with st.form("reservation"):
                st.markdown("**📅 Réserver un film (24h)**")
                resa = st.selectbox("Choisir", [f["titre"] for f in st.session_state.films])
                if st.form_submit_button("🔓 ENTRÉE - Réserver"):
                    st.success(f"{resa} réservé 24h pour toi!")
        with col3:
            st.markdown("**💬 Assistance Rapide 24h/24**")
            st.link_button("WhatsApp Assistance PLUS", "https://wa.me/242066778924")
    else:
        st.info("Passe en PLUS à 5000F pour avoir 4K, film à la demande, réservation et assistance 24h/24")

    st.divider()
    cat_f = st.selectbox("CATEGORIE", ["TOUT", "Film", "Série", "Documentaire"], key="cat_acc")
    genre_f = st.selectbox("GENRE", ["TOUS", "ANIMÉ", "SUSPENSE", "ROMANTIQUE", "GUERRE", "JEUNESSE", "ACTION"], key="genre_acc")

    films = st.session_state.films
    if cat_f!= "TOUT": films = [f for f in films if f["categorie"] == cat_f]
    if genre_f!= "TOUS": films = [f for f in films if f["genre"] == genre_f]
    if search: films = [f for f in films if search.lower() in f["titre"].lower()]

    cols = st.columns(4)
    for i, film in enumerate(films):
        # LOGIQUE SIMPLE vs PLUS
        is_4k = film.get("qualite") == "4K"
        can_watch = True
        if is_4k and st.session_state.user_tier!= "Plus":
            can_watch = False

        with cols[i % 4]:
            st.markdown('<div class="film-card">', unsafe_allow_html=True)
            st.image(film["image"], use_container_width=True)
            badge = f'<span class="badge-4k">4K</span>' if is_4k else '<span class="badge-plus">HD</span>'
            st.markdown(f"{badge} **{film['titre']}**", unsafe_allow_html=True)
            st.caption(f"{film['genre']} | {film['categorie']}")

            if not can_watch:
                st.warning("🔒 4K réservé aux PLUS (5000F)")
            else:
                if st.button("Bande annonce", key=f"b_{film['id']}"): st.video(film["trailer"])
                if st.button("Regarder", key=f"r_{film['id']}"): st.video(film["youtube"])
            st.markdown('</div>', unsafe_allow_html=True)

# ESPACE ASSOCIE
elif menu == "Espace Associé":
    st.title("Espace Associé")
    if not st.session_state.get("admin"):
        st.markdown("### 🔒 Accès sécurisé BOSS / Directeur")
        code = st.text_input("Code", type="password", key="code_seph")
        if st.button("🔓 ENTRÉE", key="btn_entree_code", use_container_width=True):
            if code == "RolVie2002":
                st.session_state["admin"] = True
                st.rerun()
            else: st.error("Mauvais code")
        st.stop()

    st.success("Bienvenue Patron!")
    if st.button("Déconnexion"): st.session_state["admin"]=False; st.rerun()

    t1, t2, t3, t4 = st.tabs(["Publier", "Gérer Films", "Accueil", "Abonnements Simple / Plus"])

    with t1:
        with st.form("pub_form_v8", clear_on_submit=True):
            titre = st.text_input("Titre *")
            cA, cB = st.columns(2)
            with cA:
                categorie = st.selectbox("Catégorie", ["Film", "Série", "Documentaire"])
                genre = st.selectbox("Genre", ["ANIMÉ", "SUSPENSE", "ROMANTIQUE", "GUERRE", "JEUNESSE", "ACTION"])
            with cB:
                annee = st.text_input("Année", "2024")
                qualite = st.selectbox("Qualité", ["HD - Pour Simple", "4K - Pour PLUS"])
                type_ac = st.selectbox("Forfait requis", ["Gratuit", "Simple - 3500F", "Plus - 5000F (4K)"])

            trailer_link = st.text_input("Lien Bande Annonce *")
            trailer_file = st.file_uploader("OU Upload Bande Annonce (illimité)", type=["mp4","mov","avi","mkv"])
            film_link = st.text_input("Lien Film Complet")
            film_file = st.file_uploader("OU Upload Film Complet (illimité - 10Go max)", type=["mp4","mkv","mov","avi"])
            image_link = st.text_input("Lien pochette")
            image_file = st.file_uploader("OU Upload Pochette", type=["jpg","png","jpeg","webp"])

            if st.form_submit_button("🔓 ENTRÉE - PUBLIER", use_container_width=True):
                if titre and (trailer_link or trailer_file):
                    final_q = "4K" if "4K" in qualite else "HD"
                    st.session_state.films.append({"id": random.randint(100,9999), "titre":titre, "categorie":categorie, "genre":genre, "annee":annee, "youtube":film_link or "upload", "trailer":trailer_link or "upload", "image":image_link or "https://via.placeholder.com/500x750/000000/E50914?text=CONGOSTREAM", "type":type_ac, "qualite":final_q})
                    st.success("Publié!"); st.balloons()
                else: st.warning("Titre + Bande annonce obligatoire")

    with t2:
        for film in st.session_state.films:
            with st.expander(f"{film['titre']} - {film['qualite']}"):
                st.image(film["image"], width=150)
                if st.button("Supprimer", key=f"del_{film['id']}"):
                    st.session_state.films = [f for f in st.session_state.films if f["id"]!= film["id"]]; st.rerun()

    with t3:
        acc = st.session_state.accueil
        acc["titre"] = st.text_input("Titre Accueil", acc["titre"])
        acc["youtube"] = st.text_input("Youtube Accueil", acc["youtube"])
        if st.button("🔓 ENTRÉE - Sauver Accueil"): st.success("Sauvé")

    with t4:
        st.subheader("Abonnements")
        simples = [a for a in st.session_state.abonnes if "Simple" in a.get("type","")]
        plus = [a for a in st.session_state.abonnes if "Plus" in a.get("type","")]
        cA, cB = st.columns(2)
        with cA:
            st.markdown(f"### Simple 3500F ({len(simples)}) - HD")
            for ab in simples: st.info(f"{ab['nom']} - {ab['id_mtn']} - Fin {ab['fin']}")
        with cB:
            st.markdown(f"### 👑 Plus 5000F ({len(plus)}) - 4K + Demande + 24h")
            for ab in plus: st.success(f"{ab['nom']} - {ab['id_mtn']} - Fin {ab['fin']}")

else: # ABONNEMENT
    st.markdown('<h1 style="color:#E50914;">Choisis ton abonnement</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="border:2px solid #333;padding:20px;border-radius:15px;background:#111;">
        <h2>SIMPLE - 3500F / 2 Mois</h2>
        <p>✅ Tous les films & séries en HD<br>✅ Accès illimité<br>❌ Pas de 4K<br>❌ Pas de film à la demande</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="border:2px solid gold;padding:20px;border-radius:15px;background:linear-gradient(135deg, #1a0a00, #000);">
        <h2 style="color:gold;">👑 PLUS - 5000F / 2 Mois</h2>
        <p>✅ Tout en SIMPLE +<br>✅ <b>Films en 4K Ultra</b><br>✅ <b>Film à la demande</b><br>✅ <b>Réservation 24h</b><br>✅ <b>Assistance rapide 24h/24</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    with st.form("abonnement_form"):
        nom = st.text_input("Ton nom")
        idm = st.text_input("ID transaction MTN (066778924)")
        type_choisi = st.selectbox("Forfait choisi", ["Simple - 3500F", "Plus - 5000F"])
        if st.form_submit_button("🔓 ENTRÉE - Activer mon abonnement", use_container_width=True):
            fin = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            st.session_state.abonnes.append({"nom":nom, "id_mtn":idm, "debut":datetime.now().strftime("%Y-%m-%d"), "fin":fin, "statut":"Actif", "type":type_choisi})
            st.success(f"Merci {nom}! Forfait {type_choisi} actif jusqu'au {fin}. Interface {'PLUS 4K' if 'Plus' in type_choisi else 'Simple HD'} débloquée!")
            st.balloons()
