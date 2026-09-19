import streamlit as st

st.set_page_config(page_title="CONGOSTREAM - BETA", layout="wide")

# --- DESIGN SANS BANDES NOIRES ---
st.markdown("""
<style>
    [data-testid="stVideo"] { background: transparent !important; }
    video { object-fit: cover !important; border-radius: 12px; width: 100% !important; }
    .stApp { background-color: #0a0a0a; }
    h1, h2, h3 { color: white !important; }
</style>
""", unsafe_allow_html=True)

st.title("🇨🇬 CONGOSTREAM - BETA")
st.caption("Le Netflix Congolais")

# --- DONNÉES DE TEST (remplace par tes vrais films après) ---
films = st.session_state.get("films", [
    {"id": 1, "titre": "Film Test 1", "trailer_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "description": "Bande annonce test"},
    {"id": 2, "titre": "Film Test 2", "trailer_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "description": "Bande annonce test 2"},
])

# --- AFFICHAGE DES FILMS ---
cols = st.columns(2)

for index, film in enumerate(films):
    with cols[index % 2]:
        st.subheader(film["titre"])
        
        # UNE SEULE VIDEO - 16:9 - 0 BANDE NOIRE
        st.video(film["trailer_url"])
        
        st.write(film["description"])
        
        if st.button(f"Voir {film['titre']}", key=f"voir_{film['id']}", use_container_width=True):
            st.session_state["film_select"] = film["id"]
            st.success(f"Tu as cliqué sur {film['titre']}")

st.divider()
st.info("✅ BETA VERSION - Site en cours de finalisation")
