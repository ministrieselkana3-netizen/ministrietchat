import streamlit as st
 
st.set_page_config(page_title="MinistrieChat - WhatsApp", page_icon="💬", layout="centered")
 
# --- STYLE WHATSAPP ---
st.markdown("""
<style>
.stApp { background-color: #ece5dd; }
.chat-bubble { background: white; padding: 10px; border-radius: 10px; margin: 5px 0; }
.header { background: #075E54; color: white; padding: 15px; border-radius: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)
 
if "page" not in st.session_state:
    st.session_state.page = "home"
if "contact" not in st.session_state:
    st.session_state.contact = None
if "contacts" not in st.session_state:
    st.session_state.contacts = ["Pasteur Jean", "Maman Marie", "Frère Paul", "Soeur Grace"]
 
# --- DONNÉES BIBLE ---
BIBLE_DATA = {
    "Jean 3:16": {"texte": "Car Dieu a tant aimé le monde qu'il a donné son Fils unique...", "explication": "C'est l'amour de Dieu pour tous. Dieu donne, il ne demande pas.", "hebreu": "Ahavah - Amour profond"},
    "Psaume 23:1": {"texte": "L'Éternel est mon berger, je ne manquerai de rien.", "explication": "Dieu nous guide et nous protège comme un berger protège ses brebis.", "hebreu": "Ra'ah - Berger, guide"},
    "Genèse 1:1": {"texte": "Au commencement, Dieu créa les cieux et la terre.", "explication": "Dieu est le créateur de tout.", "hebreu": "Bereshit - Au commencement"},
}
 
NOMS = {
    "Abraham": "Père d'une multitude - Genèse 17:5",
    "Moïse": "Tiré des eaux - Exode 2:10",
    "Jésus": "Dieu sauve - Matthieu 1:21",
    "David": "Bien-aimé - 1 Samuel 16:13",
}
 
THEMES = {
    "Foi": "Hébreux 11:1 - La foi est une ferme assurance des choses qu'on espère.",
    "Prière": "Matthieu 6:9 - Notre Père qui es aux cieux...",
    "Amour": "1 Corinthiens 13:4 - L'amour est patient, il est plein de bonté.",
    "Pardon": "Matthieu 6:14 - Si vous pardonnez aux hommes...",
}
 
# --- PAGE D'ACCUEIL ---
if st.session_state.page == "home":
    st.markdown('<div class="header"><h2>MinistrieChat</h2></div>', unsafe_allow_html=True)
 
    # Barre de recherche en haut
    search = st.text_input("🔍 Rechercher", placeholder="Rechercher une conversation...")
 
    st.write("### Discussions")
    for c in st.session_state.contacts:
        if search.lower() in c.lower() or not search:
            if st.button(f"👤 {c}  > ", key=c, use_container_width=True):
                st.session_state.contact = c
                st.session_state.page = "chat"
                st.rerun()
 
    # Bouton + caché
    with st.expander("➕ Ajouter"):
        new = st.text_input("Nom du contact")
        if st.button("Ajouter Contact"):
            if new:
                st.session_state.contacts.append(new)
                st.rerun()
 
    st.markdown("---")
    # Onglets en bas
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.button("💬\nDiscussions")
    with col2:
        st.button("🟢\nStatut")
    with col3:
        st.button("👥\nCommunauté")
    with col4:
        st.button("📞\nAppels")
    with col5:
        if st.button("📖\nBible"):
            st.session_state.page = "bible"
            st.rerun()
 
# --- PAGE CHAT ---
elif st.session_state.page == "chat":
    if st.button("⬅ Retour"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown(f'<div class="header"><h3>{st.session_state.contact}</h3></div>', unsafe_allow_html=True)
    st.write("Bonjour, que Dieu te bénisse ! 🙏")
    msg = st.text_input("Écrire un message...")
    if st.button("Envoyer"):
        st.success(f"Envoyé à {st.session_state.contact}: {msg}")
 
# --- PAGE ÉTUDE BIBLIQUE ---
elif st.session_state.page == "bible":
    if st.button("⬅ Retour Accueil"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('<div class="header"><h2>📖 Étude Biblique</h2></div>', unsafe_allow_html=True)
 
    # Barre de recherche Bible
    q = st.text_input("🔍 Recherche Bible", placeholder="Tape: amour, Jean 3:16, Abraham, hébreu...")
 
    tab1, tab2, tab3, tab4 = st.tabs(["Bible", "Thèmes", "Versets Expliqués", "Noms & Hébreu"])
 
    with tab1:
        st.write("### Toute la Bible")
        for ref, data in BIBLE_DATA.items():
            if not q or q.lower() in ref.lower() or q.lower() in data['texte'].lower():
                st.write(f"**{ref}**")
                st.write(data['texte'])
                st.write(f"*Explication:* {data['explication']}")
                st.write(f"*Hébreu:* {data['hebreu']}")
                st.write("---")
 
    with tab2:
        st.write("### Étude par Thème")
        for t, d in THEMES.items():
            if not q or q.lower() in t.lower():
                st.write(f"**{t}** - {d}")
 
    with tab3:
        st.write("### Explication des Versets")
        for ref, data in BIBLE_DATA.items():
            st.write(f"**{ref}**: {data['explication']}")
 
    with tab4:
        st.write("### Signification des Noms Bibliques & Hébreu")
        for nom, sens in NOMS.items():
            if not q or q.lower() in nom.lower():
                st.write(f"**{nom}** : {sens}")
