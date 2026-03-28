import streamlit as st
from langchain_groq import ChatGroq
from duckduckgo_search import DDGS # Plus stable que l'outil LangChain

# --- Configuration de la page ---
st.set_page_config(page_title="Accompagnement PME en RDC", layout="centered")

# Récupération sécurisée de la clé API
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    st.error("⚠️ Clé API manquante. Ajoutez GROQ_API_KEY dans les Secrets de Streamlit.")
    st.stop()

# --- Fonction de recherche simplifiée ---
def chercher_web(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except Exception:
        return "Pas d'informations web récentes disponibles."

# --- Initialisation de l'IA (Groq) ---
llm = ChatGroq(
    temperature=0.2, 
    groq_api_key=GROQ_API_KEY, 
    model_name="llama-3.3-70b-versatile"
)

# --- Interface Utilisateur ---
st.title("🚀 Expert IA : Automatisation & Droit OHADA (RDC)")
st.subheader("Vulgarisation pour PME et TPE")

menu = ["Conseil OHADA", "Automatisation Business", "Recherche de Débouchés"]
choix = st.sidebar.selectbox("Comment puis-je vous aider ?", menu)

question = st.text_area(f"Posez votre question sur : {choix}")

if st.button("Lancer l'Agent"):
    if question:
        with st.spinner("L'agent analyse le contexte en RDC..."):
            # 1. Recherche via la fonction stable
            contexte_web = chercher_web(f"RDC OHADA {choix} {question}")
            
            # 2. Construction du prompt
            system_prompt = f"""
            Tu es un consultant expert pour les PME en République Démocratique du Congo.
            Contexte actuel : {contexte_web}
            Sujet : {choix}
            Question : {question}
            
            Instructions :
            - Réponds en français de manière pédagogique.
            - Cite les principes OHADA si nécessaire.
            - Propose des solutions concrètes pour le marché congolais.
            """
            
            # 3. Génération
            reponse = llm.invoke(system_prompt)
            
            # 4. Affichage
            st.success("Analyse terminée !")
            st.markdown("### Réponse de votre Agent :")
            st.write(reponse.content)
    else:
        st.warning("Veuillez entrer une question.")

# --- Pied de page ---
st.sidebar.info("Propulsé par Groq (Llama 3). Développé par Thierry Kafun.")
