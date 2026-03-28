import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq

# --- Configuration de la page ---
st.set_page_config(page_title="Accompagnement PME en RDC", layout="centered")

# Récupération de la clé API (Utilise st.secrets pour la production)
# Pour tester en local, remplace par ta clé réelle
GROQ_API_KEY = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else "TA_CLE_GROQ_ICI"

# --- Initialisation de l'IA (Cerveau Groq) ---
# Llama-3-70b est excellent pour le raisonnement juridique OHADA
llm = ChatGroq(
    temperature=0.2, 
    groq_api_key=GROQ_API_KEY, 
    model_name="llama3-70b-8192"
)

search = DuckDuckGoSearchRun()

# --- Interface Utilisateur ---
st.title("🚀 Expert IA : Automatisation & Droit OHADA (RDC)")
st.subheader("Vulgarisation pour PME et TPE")

menu = ["Conseil OHADA", "Automatisation Business", "Recherche de Débouchés"]
choix = st.sidebar.selectbox("Comment puis-je vous aider ?", menu)

question = st.text_area(f"Posez votre question sur : {choix}")

if st.button("Lancer l'Agent"):
    if question:
        with st.spinner("L'agent analyse le web et les textes de loi..."):
            # 1. Recherche d'informations fraîches sur le contexte RDC/OHADA
            recherche_web = search.run(f"actualité RDC OHADA {choix} {question}")
            
            # 2. Construction du prompt spécialisé
            system_prompt = f"""
            Tu es un consultant expert pour les PME en République Démocratique du Congo.
            Ton but est de vulgariser des concepts complexes.
            Contexte actuel du web : {recherche_web}
            Domaine d'intervention : {choix}
            Question du client : {question}
            
            Instructions :
            - Réponds de manière professionnelle et pédagogique.
            - Pour le droit OHADA, cite les principes généraux applicables.
            - Pour l'automatisation, propose des outils gratuits ou peu coûteux.
            - Pour les débouchés, identifie des opportunités concrètes en RDC ou en Afrique centrale.
            """
            
            # 3. Génération ultra-rapide avec Groq
            reponse = llm.invoke(system_prompt)
            
            # 4. Affichage du résultat
            st.success("Analyse terminée !")
            st.markdown("### Réponse de votre Agent :")
            st.write(reponse.content)
    else:
        st.warning("Veuillez entrer une question pour continuer.")

# --- Pied de page ---
st.sidebar.info("Hébergé gratuitement sur Streamlit Cloud. Propulsé par Groq (Llama 3).Développé par Thierry Kafun")
