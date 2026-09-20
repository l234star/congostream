import streamlit as st
import os, json, random
from datetime import datetime
import cloudinary, cloudinary.uploader

st.set_page_config(page_title="CongoStream", layout="wide")

CODE_ADMIN = "JOKSAN2026"
NUMERO = "066778924"

try:
    cloudinary.config(
        cloud_name = st.secrets["cloudinary"]["cloud_name"],
        api_key = st.secrets["cloudinary"]["api_key"],
        api_secret = st.secrets["cloudinary"]["api_secret"]
    )
    OK = True
except:
    OK = False

FILMS_FILE = "films.json"
TRANSAC_FILE = "transactions.json"

def charger(nom):
    if os.path.exists(nom):
        try:
            with open(nom,"r",encoding="utf-8") as f: return json.load(f)
        except: return []
    return []
def sauver(nom, data):
    with open(nom,"w",encoding="utf-8") as f: json.dump(data,f,indent=2,ensure_ascii=False)
def upload(file, folder):
    if not file or not OK: return ""
    try:
        r = cloudinary.uploader.upload(file, resource_type="auto", folder=folder, chunk_size=6000000)
        return r.get("secure_url","")
    except Exception as e:
        st.error(f"Upload: {e}"); return ""

if "films" not in st.session_state: st.session_state.films = charger(FILMS_FILE)
if "trans" not in st.session_state: st.session_state.trans = charger(TRANSAC_FILE)
if "editing" not in st.session_state: st.session_state.editing = None
if "mes_acces" not in st.session_state: st.session_state.mes_acces = [] # films débloqués pour ce client

films = st.session_state.films

st.markdown(f'<div style="background:#000;padding:15px;border-radius:10px;"><span style="color:#E50914;font-size:32px;font-weight:900;">CONGOSTREAM</span> <span style="color:white;margin-left:15px;">By.Mr_Joksan</span> <span style="color:gray;float:right;">{len(films)} films</span></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏠 ACCUEIL CLIENTS", "➕ PUBLIER (Code)", "⚙️ GÉRER (Code)"])

# ================= ACCUEIL CLIENTS =================
with tab1:
    st.write("### 🎬 Catalogue")
    st.info(f"💡 Films gratuits = lecture directe | Films payants = Envoie argent au **{NUMERO}** + ID transaction, attente 5min max")

    if not films:
        st.warning("Aucun film publié pour l'instant")
    else:
        # Ce que le client a débloqué
        if st.session_state.mes_acces:
            st.success(f"✅ Tu as accès à: {', '.join(st.session_state.mes_acces)}")
        
        recherche = st.text_input("🔍 Rechercher")
        liste = [f for f in films if recherche.lower() in f['titre'].lower()] if recherche else films

        cols = st.columns(3)
        for i, film in enumerate(reversed(liste)):
            with cols[i % 3]:
                with st.container(border=True):
                    if film.get("image_url"): st.image(film["image_url"], use_container_width=True)
                    st.write(f"**{film['titre']}**")
                    st.caption(f"{film.get('genre','')} | {film.get('paiement','Gratuit')}")

                    # Bande annonce toujours gratuite
                    if film.get("bande_annonce_url"):
                        st.write("🎥 Bande Annonce (gratuit)")
                        st.video(film["bande_annonce_url"])

                    # FILM GRATUIT = LECTURE DIRECTE SANS CONFIRMATION
                    if film.get("paiement") == "Gratuit":
                        if film.get("film_url"):
                            st.write("🎬 Film Complet - GRATUIT")
                            st.video(film["film_url"])
                        else:
                            st.info("Film gratuit - pas de vidéo principale")
                    else:
                        # FILM PAYANT
                        a_acces = film['titre'] in st.session_state.mes_acces
                        # Vérifie si transaction confirmée
                        for t in st.session_state.trans:
                            if t['titre']==film['titre'] and t['statut']=="Confirmé":
                                if film['titre'] not in st.session_state.mes_acces:
                                    st.session_state.mes_acces.append(film['titre'])
                                    a_acces = True
                        
                        if a_acces:
                            st.success("✅ Débloqué!")
                            if film.get("film_url"): st.video(film["film_url"])
                        else:
                            st.warning(f"🔒 Payant: {film.get('paiement')}")
                            with st.form(f"pay_{film['id']}", clear_on_submit=True):
                                st.write(f"1. Envoie {film.get('paiement')} au {NUMERO}")
                                st.write("2. Mets l'ID de transaction:")
                                id_t = st.text_input("ID transaction")
                                submit = st.form_submit_button("Envoyer ID")
                                if submit and id_t:
                                    st.session_state.trans.append({"film_id":film['id'],"titre":film['titre'],"id_transaction":id_t,"statut":"En attente","date":datetime.now().strftime("%d/%m %H:%M")})
                                    sauver(TRANSAC_FILE, st.session_state.trans)
                                    st.success("Envoyé! Attends 5min max pour confirmation de l'associé")

# ================= PUBLIER BLOQUÉ =================
with tab2:
    st.subheader("Publier - Admin seulement")
    code = st.text_input("Code admin", type="password", key="pub")
    if code != CODE_ADMIN:
        st.warning("🔐 Code requis: entre JOKSAN2026")
    else:
        st.success("Accès autorisé By.Mr_Joksan")
        with st.form("add", clear_on_submit=True):
            c1,c2 = st.columns(2)
            with c1:
                titre = st.text_input("Titre *")
                genre = st.selectbox("Genre", ["Action","Aventure","Comédie","Drame","Romantique","Horreur","Thriller","Science-Fiction","Congolais","Nollywood","Africain","Telenovela","Documentaire"])
                annee = st.number_input("Année",1990,2030,2024)
                type_f = st.selectbox("Type", ["Film","Série","Anime","Documentaire"])
            with c2:
                desc = st.text_area("Description *")
                paiement = st.selectbox("Paiement", ["Gratuit","Location 500 FCFA","Location 1000 FCFA","Achat 2000 FCFA","Abonnement 5000 FCFA","MTN Money","Airtel Money","Orange Money"])
                qualite = st.selectbox("Qualité", ["HD 720p","Full HD 1080p","4K"])
            a,b,c = st.columns(3)
            with a: img = st.file_uploader("Affiche", type=["jpg","png","webp"])
            with b: ba = st.file_uploader("Bande Annonce", type=["mp4","mov"])
            with c: film_f = st.file_uploader("Film complet", type=["mp4","mkv","avi"])
            if st.form_submit_button("🚀 Publier"):
                if titre:
                    with st.spinner("Upload..."):
                        u1=upload(img,"congostream/affiches"); u2=upload(ba,"congostream/ba"); u3=upload(film_f,"congostream/films")
                        st.session_state.films.append({"id":random.randint(1000,99999),"titre":titre,"type":type_f,"genre":genre,"annee":annee,"desc":desc,"paiement":paiement,"qualite":qualite,"image_url":u1,"bande_annonce_url":u2,"trailer_url":u2,"film_url":u3,"video_url":u3 if u3 else u2,"timestamp":datetime.now().strftime("%d/%m %H:%M")})
                        sauver(FILMS_FILE, st.session_state.films)
                        st.success(f"{titre} publié! Va dans ACCUEIL pour voir"); st.balloons()

# ================= GÉRER BLOQUÉ + MODIFIER =================
with tab3:
    st.subheader("Gérer - Admin seulement")
    code2 = st.text_input("Code admin", type="password", key="ger")
    if code2 != CODE_ADMIN:
        st.warning("🔐 Code requis pour gérer")
    else:
        st.success("Mode gestion activé")
        
        # Transactions
        st.write("### 💰 Validations paiements (5min max)")
        if not st.session_state.trans: st.info("Aucune transaction")
        for t in st.session_state.trans:
            c1,c2,c3,c4,c5 = st.columns([2,2,1,1,1])
            c1.write(t['titre']); c2.write(f"ID:{t['id_transaction']}"); c3.write(t['statut'])
            if c4.button("✅ Confirmer", key=f"ok_{t['id_transaction']}"):
                t['statut']="Confirmé"; sauver(TRANSAC_FILE, st.session_state.trans); st.rerun()
            if c5.button("❌ Refuser", key=f"no_{t['id_transaction']}"):
                st.session_state.trans.remove(t); sauver(TRANSAC_FILE, st.session_state.trans); st.rerun()

        st.divider()
        st.write(f"### 📚 Films ({len(films)}) - Modifier / Supprimer")
        
        # Formulaire modifier si on a cliqué
        if st.session_state.editing:
            f_edit = next((x for x in films if x['id']==st.session_state.editing), None)
            if f_edit:
                st.write(f"✏️ Modification de: {f_edit['titre']}")
                with st.form("edit_form"):
                    nt = st.text_input("Titre", value=f_edit['titre'])
                    ng = st.selectbox("Genre", ["Action","Aventure","Comédie","Drame","Romantique","Horreur","Thriller","Science-Fiction","Congolais","Nollywood","Africain","Telenovela","Documentaire"], index=0)
                    nd = st.text_area("Description", value=f_edit.get('desc',''))
                    np = st.selectbox("Paiement", ["Gratuit","Location 500 FCFA","Location 1000 FCFA","Achat 2000 FCFA","Abonnement 5000 FCFA","MTN Money","Airtel Money","Orange Money"])
                    if st.form_submit_button("💾 Sauver modifs"):
                        f_edit['titre']=nt; f_edit['genre']=ng; f_edit['desc']=nd; f_edit['paiement']=np
                        sauver(FILMS_FILE, st.session_state.films); st.session_state.editing=None; st.success("Modifié!"); st.rerun()
                if st.button("Annuler modif"): st.session_state.editing=None; st.rerun()

        for film in reversed(films):
            with st.expander(f"{film['titre']} - {film.get('paiement')}"):
                c1,c2 = st.columns([1,2])
                with c1:
                    if film.get("image_url"): st.image(film["image_url"], width=150)
                with c2:
                    st.write(film)
                    col_a, col_b = st.columns(2)
                    if col_a.button(f"✏️ Modifier", key=f"mod_{film['id']}"):
                        st.session_state.editing = film['id']; st.rerun()
                    if col_b.button(f"🗑️ Supprimer", key=f"del_{film['id']}"):
                        st.session_state.films = [x for x in films if x['id']!=film['id']]
                        sauver(FILMS_FILE, st.session_state.films); st.rerun()
