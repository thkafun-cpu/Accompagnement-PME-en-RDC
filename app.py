import streamlit as st
from langchain_groq import ChatGroq
from duckduckgo_search import DDGS # Plus stable que l'outil LangChain

# --- Configuration de la page ---
st.set_page_config(page_title="Accompagnement PME en RDC", page_icon ="CG", layout="wide")

# --- DESIGN PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    /* Fond de la barre latérale en Bleu Azur */
    [data-testid="stSidebar"] {
        background-color: #007FFF;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Bouton Principal en Jaune Or */
    div.stButton > button:first-child {
        background-color: #F7D618;
        color: #000000;
        border-radius: 10px;
        border: 2px solid #CE1021;
        font-weight: bold;
        width: 100%;
    }
    /* Titres en Bleu */
    h1 {
        color: #007FFF;
        border-bottom: 3px solid #F7D618;
    }
    /* Encadré des réponses */
    .res-box {
        padding: 20px;
        border-radius: 10px;
        border-left: 10px solid #CE1021;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Récupération sécurisée de la clé API
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    st.error("⚠️ Clé API manquante dans les Secrets.")
    st.stop()

# --- Fonction de recherche simplifiée ---
def chercher_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except:
        return "Contexte local non disponible."

# --- Initialisation de l'IA (Groq) ---
llm = ChatGroq(
    temperature=0.2, 
    groq_api_key=GROQ_API_KEY, 
    model_name="llama-3.3-70b-versatile"
)

# --- Interface Utilisateur ---
st.sidebar.image("https://wikimedia.org", width=150)
st.sidebar.title("Options de l'Agent")

st.title("🇨🇬 Expert IA : Automatisation & Droit OHADA")
st.write("Le partenaire numérique des PME en République Démocratique du Congo.")

col1, col2 = st.columns([2, 1])

with col1:
    menu = ["Conseil OHADA", "Automatisation Business", "Recherche de Débouchés"]
    choix = st.selectbox("Sélectionnez votre domaine :", menu)
    question = st.text_area("Expliquez votre besoin ou posez votre question :", height=150)

with col2:
    st.info("**Astuce :** Soyez précis sur votre secteur d'activité (ex: Commerce à Kinshasa, Mines à Kolwezi).")

if st.button("Lancer l'analyse 🚀"):
    if question:
        with st.spinner("Recherche en cours dans le bassin du Congo..."):
            contexte = chercher_web(f"RDC OHADA {choix} {question}")
            prompt = f"Tu es un expert consultant RDC. Sujet: {choix}. Contexte: {contexte}. Question: {question}. Réponds de façon structurée."
            reponse = llm.invoke(prompt)
            
            st.success("Analyse terminée !")
            # Affichage dans un bloc stylisé
            st.markdown(f'<div class="res-box">{reponse.content}</div>', unsafe_allow_html=True)
    else:
        st.warning("Veuillez entrer une question.")

st.sidebar.markdown("---")
st.sidebar.write("Développé par **Thierry Kafun**")
