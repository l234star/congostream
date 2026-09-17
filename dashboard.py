import streamlit as st
import json, os
from datetime import datetime, timedelta

st.set_page_config(page_title="CONGOSTREAM", layout="wide", page_icon="🎬")

FICHIER_VIDEOS = "videos.json"
FICHIER_ABOS = "abonnements.json"
MDP_ADMIN = "RolVie2002"

def charger(fichier, defaut):
    if os.path.exists(fichier):
        with open(fichier, "r") as f:
            return json.load(f)
    return defaut

def sauver(fichier, data):
    with open(fichier, "w") as f:
        json.dump(data, f, indent=2)

videos = charger(FICHIER_VIDEOS, [
    {"titre": "Boruto x Naruto - Extrait", "lien": "https://www.youtube.com/watch?v=Q5l9Y8R8f3E", "premium": False},
    {"titre": "Boruto - Film Complet", "lien": "https://www.youtube.com/watch?v=Q5l9Y8R8f3E", "premium": True},
])
abos = charger(FICHIER_ABOS, [])

def verifier_abo(transaction_id):
    for abo in abos:
        if abo["id"] == transaction_id:
            date_fin = datetime.strptime(abo["fin"], "%Y-%m-%d")
            if datetime.now() <= date_fin:
                jours_restants = (date_fin - datetime.now()).days
                return True, jours_restants, abo["fin"]
            else:
                return False, 0, abo["fin"]
    return False, 0, ""

menu = st.sidebar.selectbox("Menu", ["🎬 Voir les films", "🔑 Espace Associé"])

if menu == "🎬 Voir les films":
    st.title("🎬 CONGOSTREAM - 3500F / 2 Mois")
    
    st.subheader("🟢 Gratuit")
    for v in videos:
        if not v["premium"]:
            st.write(f"**{v['titre']}**")
            st.video(v["lien"])

    st.divider()
    st.markdown("""
    ### 🔒 Premium - Abonnement 2 Mois = 3500 FCFA
    **MTN Mobile Money : 066778924** | Tape *105#
    """)

    col1, col2 = st.columns(2)
    with col1:
        tid_input = st.text_input("Entre ton ID de transaction MTN :")
        if st.button("✅ Activer mon abonnement 2 mois"):
            if tid_input:
                existe, _, _ = verifier_abo(tid_input)
                if not existe:
                    fin = datetime.now() + timedelta(days=60)
                    abos.append({"id": tid_input, "debut": datetime.now().strftime("%Y-%m-%d"), "fin": fin.strftime("%Y-%m-%d")})
                    sauver(FICHIER_ABOS, abos)
                    st.success(f"Abonnement activé jusqu'au {fin.strftime('%d/%m/%Y')} !")
                    st.session_state["mon_id"] = tid_input
                else:
                    st.session_state["mon_id"] = tid_input
                    st.info("Abonnement retrouvé !")
            else:
                st.warning("Entre ton ID")

    with col2:
        mon_id = st.session_state.get("mon_id", "")
        if mon_id:
            valide, jours, date_fin = verifier_abo(mon_id)
            if valide:
                st.success(f"✅ Abonnement valide jusqu'au {date_fin} - Il reste {jours} jours")
                st.subheader("🎥 Films Premium")
                for v in videos:
                    if v["premium"]:
                        st.write(f"**{v['titre']}**")
                        st.video(v["lien"])
            else:
                st.error(f"❌ Abonnement expiré depuis le {date_fin}. Veuillez repayer 3500F au 066778924")
                st.session_state["mon_id"] = ""

else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:30px; border-radius:15px; color:white; text-align:center;">
        <h1>👋 Bienvenue Monsieur Seph NTOUMOU</h1>
        <h3>Votre clientèle attend du nouveau contenu !</h3>
    </div>
    """, unsafe_allow_html=True)
    
    mdp = st.text_input("Mot de passe :", type="password")
    if mdp == MDP_ADMIN:
        st.success("Accès autorisé")
        st.balloons()
        
        st.subheader("💰 Gestion des abonnements (3500F / 2 mois)")
        st.write(f"Total abonnés : {len(abos)}")
        for abo in abos:
            fin = datetime.strptime(abo["fin"], "%Y-%m-%d")
            statut = "✅ Actif" if datetime.now() <= fin else "❌ Expiré"
            st.write(f"ID: {abo['id']} | Fin: {abo['fin']} | {statut}")

        st.divider()
        st.subheader("📤 Publier contenu")
        with st.form("ajout"):
            titre = st.text_input("Titre")
            lien = st.text_input("Lien YouTube")
            premium = st.checkbox("Premium")
            if st.form_submit_button("Publier"):
                videos.append({"titre": titre, "lien": lien, "premium": premium})
                sauver(FICHIER_VIDEOS, videos)
                st.success("Publié !")
                st.rerun()
