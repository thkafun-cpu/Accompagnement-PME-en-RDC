import streamlit as st
from langchain_groq import ChatGroq
from duckduckgo_search import DDGS
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Agent IA - PME RDC", page_icon="🇨🇬", layout="wide")

# --- CSS AUX COULEURS DU DRAPEAU ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #007FFF; color: white; }
    div.stButton > button { background-color: #F7D618; color: black; font-weight: bold; width: 100%; border: 2px solid #CE1021; }
    .event-box { padding: 15px; border: 2px dashed #F7D618; background-color: #e3f2fd; border-radius: 10px; margin-bottom: 20px; }
    h1, h2 { color: #007FFF; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
page = st.sidebar.radio("Navigation", ["🤖 Agent IA", "🤝 Accompagnement Spécifique", "📅 Newsletter & Événements"])

# --- LOGIQUE IA (Code précédent optimisé) ---
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "TA_CLE_ICI")
llm = ChatGroq(temperature=0.2, groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

# --- PAGE 1 : AGENT IA ---
if page == "🤖 Agent IA":
    st.title("🇨🇬 Expert IA : Conseil & Automatisation")
    with st.form("ia_form"):
        menu = ["Conseil OHADA", "Automatisation Business", "Recherche de Débouchés"]
        choix = st.selectbox("Domaine d'expertise :", menu)
        question = st.text_area("Votre question :")
        valider = st.form_submit_button("Interroger l'IA 🚀")
        
    if valider and question:
        with st.spinner("Analyse en cours..."):
            reponse = llm.invoke(f"Expert RDC. Sujet: {choix}. Question: {question}")
            st.success("Conseil généré !")
            st.write(reponse.content)

# --- PAGE 2 : ACCOMPAGNEMENT (FORMULAIRE) ---
elif page == "🤝 Accompagnement Spécifique":
    st.title("🎯 Solliciter un Accompagnement")
    st.write("Remplissez ce formulaire pour booster votre visibilité et obtenir un conseil sur mesure.")
    
    with st.form("form_accompagnement"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            nat = st.text_input("Nationalité", value="Congolaise")
            ville = st.text_input("Ville de résidence (RDC)")
        
        with col2:
            secteur = st.selectbox("Type de business", [
                "Technologies de l'information", "Agropastoral", 
                "Transformation micro-industrielle", "Production micro-industrielle", 
                "Commerce", "Services"
            ])
            nom_biz = st.text_input("Nom du business (si lancé)")
            personnel = st.number_input("Nombre de personnels", min_value=0, step=1)
        
        besoin = st.multiselect("Services souhaités", ["Publicité Site Web", "Publicité Facebook", "Publicité LinkedIn", "Accompagnement Juridique"])
        
        submit_biz = st.form_submit_button("Envoyer ma demande d'enregistrement")
        
        if submit_biz:
            # Ici, on simule l'enregistrement. Idéalement : envoyer vers Supabase ou Email
            st.balloons()
            st.success(f"Merci {prenom} ! Votre demande pour '{nom_biz}' a été enregistrée. Notre équipe vous contactera sous 48h.")
            # LOGIQUE DE STOCKAGE : Tu peux utiliser requests.post vers un Webhook Make ici

# --- PAGE 3 : NEWSLETTER ---
elif page == "📅 Newsletter & Événements":
    st.title("📢 Actualités & Événements")
    
    st.markdown("""
    <div class="event-box">
        <h4>🗓️ Webinaire : Automatiser sa comptabilité avec Python</h4>
        <p><b>Date :</b> 15 Avril 2024 à 14h (Heure de Kinshasa)<br>
        <i>Gratuit pour les membres enregistrés.</i></p>
    </div>
    <div class="event-box">
        <h4>🗓️ Forum PME & Digital - Lubumbashi</h4>
        <p><b>Date :</b> 22 Mai 2024<br>
        Rencontre physique des entrepreneurs du Katanga.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("S'abonner à la Newsletter")
    email_news = st.text_input("Entrez votre email pour recevoir les alertes :")
    if st.button("S'abonner"):
        st.toast("Email enregistré ! Bienvenue dans la communauté.")

st.sidebar.markdown("---")
st.sidebar.write("Développé par **Thierry Kafun**")
