import streamlit as st
from datetime import datetime, timedelta
import random
import time

st.set_page_config(page_title="CONGOSTREAM", page_icon="🎬", layout="wide")

# --- INTRO VERT JAUNE ROUGE ANIMÉE (une seule fois) ---
if "intro_done" not in st.session_state:
    st.markdown("""
    <style>
        .intro-container {
            position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
            z-index: 999999; display: flex; align-items: center; justify-content: center;
            background: #000; overflow: hidden; animation: introFadeOut 1s ease 4s forwards;
        }
        .color-bar { height: 100vh; width: 33.33%; position: absolute; top: 0; transform: translateY(100%); }
        .bar-green { background: #009543; left: 0; animation: slideUp 0.8s ease 0.2s forwards; }
        .bar-yellow { background: #FBDE4A; left: 33.33%; animation: slideUp 0.8s ease 0.5s forwards; }
        .bar-red { background: #DC241F; left: 66.66%; animation: slideUp 0.8s ease 0.8s forwards; }
        .intro-logo {
            z-index: 10; font-size: 60px; font-weight: 900; color: white; letter-spacing: 8px;
            text-shadow: 0 0 30px rgba(0,0,0,0.9); opacity: 0; animation: logoZoom 1s ease 1.5s forwards;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .intro-logo span { color: #FBDE4A; }
        @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0%); } }
        @keyframes logoZoom { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }
        @keyframes introFadeOut { from { opacity: 1; } to { opacity: 0; visibility: hidden; } }
        .africa-pattern { position: absolute; width: 100%; height: 100%; opacity: 0.05; background-image: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h40v40H0z M40 40h40v40H40z' fill='%23FBDE4A'/%3E%3C/svg%3E"); }
    </style>
    <div class="intro-container">
        <div class="africa-pattern"></div>
        <div class="color-bar bar-green"></div>
        <div class="color-bar bar-yellow"></div>
        <div class="color-bar bar-red"></div>
        <div class="intro-logo">CONGO<span>STREAM</span></div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(4.5)
    st.session_state.intro_done = True
    st.rerun()

# --- FOND LIVE AFRICAIN NOIR ROUGE + TOUCHES VERT JAUNE ROUGE ---
st.markdown("""
<style>
    .stApp {
        background: #000000;
        background-image: 
            radial-gradient(circle at 15% 20%, rgba(0,149,67,0.18) 0%, transparent 35%),
            radial-gradient(circle at 50% 50%, rgba(251,222,74,0.10) 0%, transparent 40%),
            radial-gradient(circle at 85% 80%, rgba(220,36,31,0.25) 0%, transparent 40%),
            linear-gradient(180deg, rgba(0,0,0,0.9) 0%, #000 100%);
        background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='60' font-size='30' opacity='0.03'%3E◍⬢⬣⬔%3C/text%3E%3C/svg%3E");
        animation: drift 60s linear infinite; pointer-events: none; z-index: 0;
    }
    @keyframes drift { from { background-position: 0 0; } to { background-position: 500px 500px; } }
    
    .netflix-red { color: #E50914; font-weight: 900; font-size: 42px; letter-spacing: 3px; text-shadow: 0 0 25px #E50914, 0 0 10px #FBDE4A; }
    .boss-badge { background: linear-gradient(90deg, #009543, #FBDE4A, #DC241F); color: black; font-weight: 900; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    .film-card { background: rgba(18,18,18,0.92); border-radius: 14px; padding: 12px; border: 1px solid #333; backdrop-filter: blur(12px); position: relative; overflow: hidden; }
    .film-card::after { content: ""; position: absolute; top: 0; left: 0; height: 3px; width: 100%; background: linear-gradient(90deg, #009543, #FBDE4A, #DC241F); }
    .film-card:hover { transform: translateY(-10px) scale(1.03); border-color: #E50914; box-shadow: 0 15px 35px rgba(229,9,20,0.5), 0 0 20px rgba(251,222,74,0.2); transition: 0.4s; }
    .live-dot { height: 12px; width: 12px; background: #009543; border-radius: 50%; display: inline-block; animation: pulseAfrica 1.2s infinite; border: 2px solid #FBDE4A; }
    @keyframes pulseAfrica { 0% { box-shadow: 0 0 0 0 rgba(0,149,67,0.8); } 70% { box-shadow: 0 0 0 12px rgba(0,149,67,0); } 100% { box-shadow: 0 0 0 0 rgba(0,149,67,0); } }
    .stButton>button { background: linear-gradient(90deg, #E50914, #b81d24); color: white; font-weight: bold; border-radius: 8px; border: none; }
    .stFileUploader { background: rgba(255,255,255,0.05); border-radius: 10px; border: 1px dashed #FBDE4A; }
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
if "films" not in st.session_state:
    st.session_state.films = [
        {"id":1, "titre": "Boruto: Naruto Next", "categorie": "Série", "genre": "ANIMÉ", "annee": "2024", "youtube": "https://www.youtube.com/watch?v=Qp3b-Rhse9k", "trailer": "https://www.youtube.com/watch?v=Qp3b-Rhse9k", "image": "https://image.tmdb.org/t/p/w500/3V4kLQg0kFFjRfyGuGSK4U8ONr.jpg", "type": "Premium", "video_file": None},
    ]
if "accueil" not in st.session_state:
    st.session_state.accueil = {"titre": "EXCLUSIVITÉ CONGO - LE FILM DE L'ANNÉE", "desc": "BOSS, votre plateforme est LIVE. Vert Jaune Rouge pour le peuple.", "youtube": "https://www.youtube.com/watch?v=Qp3b-Rhse9k", "image": ""}
if "abonnes" not in st.session_state:
    st.session_state.abonnes = [{"nom": "Client Test", "id_mtn": "MTN123456", "debut": "2026-09-01", "fin": "2026-11-01", "statut": "Actif"}]

# --- HEADER BOSS / DIRECTEUR ---
c1, c2, c3 = st.columns([2.5, 3, 1.5])
with c1: st.markdown('<div class="netflix-red">CONGOSTREAM <span class="live-dot"></span></div>', unsafe_allow_html=True)
with c2: search = st.text_input("", placeholder="🔍 Rechercher film, série, animé...", label_visibility="collapsed")
with c3: menu = st.selectbox("", ["Acc
