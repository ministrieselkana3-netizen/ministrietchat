import streamlit as st

st.set_page_config(page_title="MinistrieChat", page_icon="💬", layout="wide")

# --- STYLE WHATSAPP ---
st.markdown("""
<style>
.stApp {background:#efeae2;}
.chat-header{background:#075e54;color:white;padding:10px;border-radius:10px;display:flex;justify-content:space-between;align-items:center}
.msg-in{background:white;padding:8px 12px;border-radius:10px;margin:5px;max-width:70%}
.msg-out{background:#dcf8c6;padding:8px 12px;border-radius:10px;margin:5px;margin-left:auto;max-width:70%;text-align:right}
.bible-box{background:white;padding:15px;border-radius:10px}
</style>
""", unsafe_allow_html=True)

# --- ETAT ---
if "user" not in st.session_state: st.session_state.user=None
if "contacts" not in st.session_state: st.session_state.contacts=[]  # vide au debut
if "messages" not in st.session_state: st.session_state.messages={}
if "current" not in st.session_state: st.session_state.current=None

BIBLE_66 = [
"Genèse","Exode","Lévitique","Nombres","Deutéronome","Josué","Juges","Ruth","1 Samuel","2 Samuel","1 Rois","2 Rois","1 Chroniques","2 Chroniques","Esdras","Néhémie","Esther","Job","Psaumes","Proverbes","Ecclésiaste","Cantique","Ésaïe","Jérémie","Lamentations","Ézéchiel","Daniel","Osée","Joël","Amos","Abdias","Jonas","Michée","Nahum","Habacuc","Sophonie","Aggée","Zacharie","Malachie",
"Matthieu","Marc","Luc","Jean","Actes","Romains","1 Corinthiens","2 Corinthiens","Galates","Éphésiens","Philippiens","Colossiens","1 Thessaloniciens","2 Thessaloniciens","1 Timothée","2 Timothée","Tite","Philémon","Hébreux","Jacques","1 Pierre","2 Pierre","1 Jean","2 Jean","3 Jean","Jude","Apocalypse"
]

# --- CONNEXION ---
if not st.session_state.user:
    st.title("💬 MinistrieChat")
    st.subheader("Crée ton compte avec ton numéro")
    numero = st.text_input("📱 Ton Numéro (ex: +243...)")
    nom = st.text_input("👤 Ton Nom")
    code = st.text_input("🔑 Crée un Code (4 chiffres)", type="password")
    gmail = st.text_input("📧 Ton Gmail (si tu en as)")
    if st.button("✅ Ouvrir mon compte"):
        if numero and nom and code:
            st.session_state.user={"numero":numero,"nom":nom,"gmail":gmail}
            st.success(f"Bienvenue {nom} ! Ton numéro {numero} est reconnu.")
            st.rerun()
        else:
            st.warning("Remplis Numéro, Nom et Code")
    st.stop()

# --- MENU PRINCIPAL ---
user = st.session_state.user
st.sidebar.markdown(f"👤 **{user['nom']}**\n📱 {user['numero']}\n📧 {user['gmail'] or 'Pas de Gmail lié'}")

onglet = st.sidebar.radio("Menu", ["💬 Discussions","📞 Appels","👥 Communauté","🟢 Statut","📖 Bible","⚙️ Paramètres"])

# --- RECHERCHE AVEC BOUTON ENVOI ---
st.markdown("### 🔍 Recherche")
col1,col2 = st.columns([4,1])
with col1:
    recherche = st.text_input("Rechercher...", label_visibility="collapsed", key="rech")
with col2:
    if st.button("➤ Envoyer"):
        st.success(f"Recherche : {recherche}")

# --- DISCUSSIONS ---
if onglet == "💬 Discussions":
    st.markdown(f"### 💬 Discussions - {user['nom']}")
    if not st.session_state.contacts:
        st.info("Aucune discussion pour le moment. Commence une nouvelle discussion !")
    # Nouvelle discussion
    new_num = st.text_input("➕ Nouveau numéro pour discuter")
    new_nom = st.text_input("Nom du contact")
    if st.button("➕ Ajouter et Discuter"):
        if new_num:
            st.session_state.contacts.append({"numero":new_num,"nom":new_nom or new_num})
            st.session_state.current = new_num
            st.rerun()
    for c in st.session_state.contacts:
        if st.button(f"💬 {c['nom']} - {c['numero']}", key=c['numero']):
            st.session_state.current = c['numero']
    # Zone chat
    if st.session_state.current:
        contact = [x for x in st.session_state.contacts if x['numero']==st.session_state.current][0]
        st.markdown(f"<div class='chat-header'><span>👤 {contact['nom']}</span><span>📹 📞</span></div>", unsafe_allow_html=True)
        # boutons appel
        c1,c2 = st.columns(2)
        if c1.button("📞 Appel Audio"): st.info(f"Appel audio vers {contact['nom']}...")
        if c2.button("📹 Appel Vidéo"): st.info(f"Appel vidéo vers {contact['nom']}...")
        msgs = st.session_state.messages.get(st.session_state.current, [])
        for m in msgs:
            st.markdown(f"<div class='msg-out'>{m}</div>", unsafe_allow_html=True)
        # Barre WhatsApp
        colE, colP, colT, colM = st.columns([1,1,6,1])
        with colE:
            if st.button("😊"): st.info("Emoji")
        with colP:
            if st.button("📎"): st.info("Joindre fichier")
        with colT:
            texte = st.text_input("Écris un message...", label_visibility="collapsed", key="txtmsg")
        with colM:
            if texte:
                if st.button("➤"): 
                    st.session_state.messages.setdefault(st.session_state.current, []).append(texte)
                    st.rerun()
            else:
                if st.button("🎤"): st.info("Enregistrement vocal...")

elif onglet == "📞 Appels":
    st.title("📞 Appels")
    st.info("Tes appels audio et vidéo vont apparaître ici.")
    st.button("📞 Nouvel appel audio")
    st.button("📹 Nouvel appel vidéo")

elif onglet == "👥 Communauté":
    st.title("👥 Communauté")
    st.write("Groupes de l'église, prières, annonces.")
    st.button("➕ Créer une communauté")

elif onglet == "🟢 Statut":
    st.title("🟢 Statut")
    st.write("Partage un verset ou une photo.")
    st.text_input("Ton statut du jour...")
    if st.button("Publier mon statut"): st.success("Statut publié !")

elif onglet == "📖 Bible":
    st.title("📖 Bible Complète - 66 Livres")
    st.write(f"Total: {len(BIBLE_66)} livres - 39 Ancien Testament + 27 Nouveau Testament")
    livre = st.selectbox("Choisis un livre", BIBLE_66)
    chapitre = st.number_input("Chapitre", min_value=1, value=1)
    if st.button("📖 Lire"):
        st.markdown(f"<div class='bible-box'><h3>{livre} {chapitre}</h3><p>Jean 3:16 - Car Dieu a tant aimé le monde qu'il a donné son Fils unique, afin que quiconque croit en lui ne périsse point, mais qu'il ait la vie éternelle.</p><p><i>Verset d'exemple - Version complète en cours</i></p></div>", unsafe_allow_html=True)
    st.write("---")
    st.write("📚 Liste des 66 livres :")
    st.write(", ".join(BIBLE_66))

elif onglet == "⚙️ Paramètres":
    st.title("⚙️ Paramètres")
    st.write(f"Nom: {user['nom']}")
    st.write(f"Numéro reconnu: {user['numero']}")
    st.write(f"Gmail lié: {user['gmail']}")
    if st.button("Déconnexion"): 
        st.session_state.user=None
        st.rerun()
