import streamlit as st
import streamlit.components.v1 as components
 
st.set_page_config(page_title="MinistrieChat - WhatsApp", page_icon="💬", layout="centered")
 
# Cache le menu Streamlit pour que ça ressemble à une vraie app
st.markdown("<style>#MainMenu, footer, header{visibility:hidden}</style>", unsafe_allow_html=True)
 
HTML = open("app.html", encoding="utf-8").read() if False else r"""
<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui,sans-serif} body{background:#efeae2} header{background:#fff;padding:10px 12px}
.logo{font-weight:800;font-size:20px}.logo span{color:#25D366} .search{margin-top:8px;background:#f0f2f5;border-radius:25px;padding:10px 14px} .search input{border:none;outline:none;background:transparent;width:88%}
.tabs{display:flex;background:#fff} .tabs button{flex:1;padding:12px;border:none;background:none;font-weight:700;color:#8696a0} .tabs button.active{color:#25D366;border-bottom:3px solid #25D366}
.chat-item{display:flex;gap:12px;padding:12px;background:#fff;border-bottom:1px solid #eee;align-items:center;cursor:pointer} .avatar{width:48px;height:48px;border-radius:50%;object-fit:cover;background:#ddd;display:flex;align-items:center;justify-content:center}
.msg-bar{position:fixed;bottom:0;left:0;right:0;background:#efeae2;padding:6px 8px;display:flex;gap:6px;z-index:20} .input-box{flex:1;background:#fff;border-radius:25px;padding:6px 8px;display:flex;gap:4px;align-items:center} .input-box input{flex:1;border:none;outline:none} .mic{width:48px;height:48px;border-radius:50%;background:#25D366;color:#fff;border:none;font-size:20px;flex-shrink:0}
.panel{position:fixed;bottom:62px;left:0;right:0;background:#fff;border-radius:16px 16px 0 0;padding:10px;max-height:45vh;overflow:auto;z-index:25} .grid{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;font-size:26px;text-align:center} .rec{position:fixed;bottom:62px;left:10px;right:10px;background:#fff;border-radius:16px;padding:14px;z-index:30;box-shadow:0 4px 20px rgba(0,0,0,.2)} .rec-bottom{display:flex;gap:12px;margin-top:12px} .btn{width:100%;padding:12px;background:#25D366;color:#fff;border:none;border-radius:10px;font-weight:700;margin:8px 0} .set-item{display:flex;gap:14px;padding:13px 0;border-bottom:1px solid #f5f5f5} .hidden{display:none} input[type=text],input[type=tel]{width:100%;padding:12px;border:1px solid #ddd;border-radius:10px;margin:6px 0}
</style></head><body>
<div id="auth" style="padding:20px;text-align:center;background:#fff"><img id="logoPreview" src="https://via.placeholder.com/110/25D366/ffffff?text=MN" style="width:110px;height:110px;border-radius:50%;object-fit:cover"><h2>Crée ton identité</h2><label style="background:#f0f2f5;padding:8px 14px;border-radius:20px;display:inline-block;cursor:pointer">📷 Choisir photo de profil<input type="file" id="photoInput" accept="image/*" style="display:none"></label><input type="text" id="nameInput" placeholder="Ton nom complet ex: Moïse NkG"><input type="tel" id="phoneInput" placeholder="Numéro WhatsApp"><input type="text" id="bioInput" placeholder="Quoi de neuf ?"><button class="btn" onclick="saveProfile()">ENTRER DANS L'APP ✓</button></div>
<div id="app" class="hidden">
<header><div style="display:flex;justify-content:space-between"><div class="logo">WhatsApp</div><div style="display:flex;gap:14px;font-size:20px"><span>📷</span><span onclick="showSettings()">⋮</span></div></div><div class="search">🔍 <input id="searchInput" placeholder="Demander à Meta AI ou rechercher" oninput="doSearch(this.value)"></div></header>
<div class="tabs"><button class="active" onclick="switchTab('disc',this)">Discussions</button><button onclick="switchTab('appels',this)">Appels</button><button onclick="switchTab('comm',this)">Communautés</button><button onclick="switchTab('bible',this)">Bible</button></div>
<main id="mainContent"></main>
<div id="chatView" class="hidden"><div style="background:#fff;padding:10px;display:flex;gap:10px;align-items:center"><button onclick="backToList()">←</button><img id="chatAvatar" class="avatar" style="width:36px;height:36px"><b id="chatName"></b></div><div id="messages" style="padding:10px;min-height:50vh"></div>
<div class="msg-bar"><div class="input-box"><button onclick="togglePanel()" style="border:none;background:none;font-size:22px">😊</button><input id="msgInput" placeholder="Message" oninput="checkSend(this)"><button onclick="toggleAttach()" style="border:none;background:none;font-size:20px">📎</button><button onclick="document.getElementById('camInput').click()" style="border:none;background:none;font-size:20px">📷</button><input type="file" id="camInput" accept="image/*" style="display:none" onchange="sendPhoto(event)"></div><button class="mic" id="micBtn" onclick="startVoice()">🎤</button></div>
<div id="emojiPanel" class="panel hidden"><div style="display:flex;gap:8px"><button style="flex:1;padding:8px;border:none;border-radius:20px;background:#25D366;color:#fff" onclick="panelTab('emoji',this)">Emoji</button><button style="flex:1;padding:8px;border:none;border-radius:20px;background:#f0f2f5" onclick="panelTab('gif',this)">GIF</button><button style="flex:1;padding:8px;border:none;border-radius:20px;background:#f0f2f5" onclick="panelTab('sticker',this)">Sticker</button></div><div id="panelEmoji" class="grid" style="margin-top:10px"></div><div id="panelGif" class="hidden" style="margin-top:10px"></div><div id="panelSticker" class="hidden" style="margin-top:10px"><button style="padding:8px 14px;border-radius:20px;background:#25D366;color:#fff;border:none">+ Créer un sticker</button><div class="grid" style="margin-top:10px"></div></div></div>
<div id="attachPanel" class="panel hidden"><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;text-align:center"><div onclick="document.getElementById('galInput').click()">🖼️<br>Galerie</div><div onclick="document.getElementById('camInput').click()">📷<br>Caméra</div><div onclick="shareLocation()">📍<br>Localisation</div><div onclick="sendContact()">👤<br>Contact</div><div onclick="document.getElementById('docInput').click()">📄<br>Document</div><div onclick="createPoll()">📊<br>Sondage</div><div onclick="createEvent()">📅<br>Événement</div></div><input type="file" id="galInput" accept="image/*" style="display:none" onchange="sendPhoto(event)"><input type="file" id="docInput" style="display:none" onchange="alert('Document envoyé: '+this.files[0].name)"></div>
<div id="recPanel" class="rec hidden"><div style="display:flex;justify-content:space-between"><b id="recTimer">0:00</b><span id="wave">...........</span><span>①</span></div><div class="rec-bottom"><button onclick="cancelVoice()" style="width:48px;height:48px;border-radius:50%;background:#ffe6e6;border:none">🗑️</button><button id="pauseBtn" onclick="togglePause()" style="flex:1;padding:12px;border:none;border-radius:20px;background:#f0f2f5;font-weight:700">⏸️ Pause</button><button onclick="sendVoice()" style="width:48px;height:48px;border-radius:50%;background:#25D366;color:#fff;border:none">➤</button></div></div>
</div>
<div id="settingsView" class="hidden" style="background:#fff;padding:14px"><button onclick="backToList()">← Paramètres</button><div style="text-align:center;padding:14px"><img id="setAvatar" style="width:110px;height:110px;border-radius:50%;object-fit:cover"><div style="background:#f0f2f5;padding:6px 10px;border-radius:20px;display:inline-block;margin-top:6px">Quoi de neuf ?</div><h2 id="setName">Moïse NkG ∨</h2><p id="setBio" style="color:#666;font-size:13px"></p></div>
<div class="set-item">💎 <div><b>Abonnements</b><br><span style="color:#666;font-size:13px">Découvrez les avantages premium</span></div></div>
<div class="set-item">💻 <div><b>Appareils connectés</b><br><span style="color:#666;font-size:13px">Utilisez WhatsApp sur d'autres appareils</span></div></div>
<div class="set-item">🔑 <div><b>Compte</b><br><span style="color:#666;font-size:13px">Notifications de sécurité, changement de numéro</span></div></div>
<div class="set-item">🔒 <div><b>Confidentialité</b><br><span style="color:#666;font-size:13px">Comptes bloqués, messages éphémères</span></div></div>
<div class="set-item">👥 <div><b>Listes</b><br><span style="color:#666;font-size:13px">Gérez les personnes et les groupes</span></div></div>
<div class="set-item">💬 <div><b>Discussions</b><br><span style="color:#666;font-size:13px">Historique, fond d'écran</span></div></div>
<div class="set-item">🗄️ <div><b>Stockage et données</b><br><span style="color:#666;font-size:13px">Utilisation réseau, téléchargement auto.</span></div></div>
<div class="set-item">🛡️ <div><b>Contrôle parental</b><br><span style="color:#666;font-size:13px">Paramètres pour votre famille</span></div></div>
<div class="set-item">♿ <div><b>Accessibilité</b><br><span style="color:#666;font-size:13px">Augmenter le contraste, animation</span></div></div>
<div class="set-item">🌐 <div><b>Langue de l'application</b><br><span style="color:#666;font-size:13px">Français (langue de l'appareil)</span></div></div>
<div class="set-item">❓ <div><b>Aide et commentaires</b><br><span style="color:#666;font-size:13px">Pages d'aide, nous contacter</span></div></div>
<div class="set-item">👥 <div><b>Inviter une personne</b></div></div>
<div class="set-item">🔄 <div><b>Mises à jour de l'application</b></div></div>
<div class="set-item">∞ <div><b>Espace Comptes</b><br><span style="color:#666;font-size:13px">WhatsApp, Facebook, Instagram</span></div></div>
<button class="btn" onclick="alert('Installer: Menu navigateur > Installer')">⬇️ INSTALLER L'APPLICATION</button>
</div>
</div>
<script>
let user=JSON.parse(localStorage.getItem('user')||'null'); if(user)showApp();
let photoData=''; document.getElementById('photoInput').addEventListener('change',e=>{let r=new FileReader();r.onload=()=>{photoData=r.result;document.getElementById('logoPreview').src=photoData};r.readAsDataURL(e.target.files[0])});
function saveProfile(){let n=document.getElementById('nameInput').value.trim(),p=document.getElementById('phoneInput').value.trim(),b=document.getElementById('bioInput').value.trim(); if(!n||!p||!photoData){alert('Mets ton nom, numéro et photo de profil !');return} user={name:n,phone:p,bio:b||'Quoi de neuf ?',photo:photoData};localStorage.setItem('user',JSON.stringify(user));showApp()}
function showApp(){document.getElementById('auth').classList.add('hidden');document.getElementById('app').classList.remove('hidden');document.getElementById('setAvatar').src=user.photo;document.getElementById('setName').textContent=user.name+' ∨';document.getElementById('setBio').textContent=user.bio+' • '+user.phone;renderList()}
let chats=[{n:'Apôtre Moïse NKG',m:'Bienvenue dans Ministries 🙏',a:'https://via.placeholder.com/100/FFD700/000?text=MN'},{n:'Famille NKG',m:'Prière à 19h',a:'https://via.placeholder.com/100/25D366/fff?text=F'},{n:'Groupe Louange',m:'Nouveau chant 🎵',a:'https://via.placeholder.com/100/128C7E/fff?text=L'}];
let curTab='disc';
function renderList(){let el=document.getElementById('mainContent');let html='';
if(curTab==='disc')html=chats.map((c,i)=>`<div class="chat-item" onclick="openChat(${i})"><img class="avatar" src="${c.a}"><div style="flex:1"><b>${c.n}</b><br><span style="color:#666;font-size:13px">${c.m}</span></div><span style="color:#25D366;font-size:12px">10:41</span></div>`).join('');
if(curTab==='appels')html=`<div style="padding:16px"><button class="btn" onclick="alert('Appel lancé')">📞 Nouvel appel</button>${chats.map(c=>`<div class="chat-item"><img class="avatar" src="${c.a}"><div style="flex:1"><b>${c.n}</b><br><span>Appel vocal • hier</span></div><span>📞</span></div>`).join('')}</div>`;
if(curTab==='comm')html=`<div style="padding:16px"><h3>Communautés</h3>${chats.map(c=>`<div class="chat-item" onclick="openChat(0)"><img class="avatar" src="${c.a}"><div><b>${c.n}</b><br><span>12 membres</span></div></div>`).join('')}</div>`;
if(curTab==='bible')html=`<div style="padding:16px"><h3>📖 Bible</h3><button class="btn" onclick="alert('Jean 3:16 - Car Dieu a tant aimé le monde...')">Jean 3:16</button><button class="btn" onclick="alert('Psaume 23 - L Eternel est mon berger')">Psaume 23</button><button class="btn" onclick="alert('Genèse 1:1 - Au commencement Dieu créa...')">Genèse 1</button><div style="margin-top:10px;background:#fff;padding:12px;border-radius:12px"><b>Dictionnaire Biblique</b><br>Amour, Foi, Grâce, Prière...</div></div>`;
el.innerHTML=html}
function switchTab(t,btn){curTab=t;document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('active'));btn.classList.add('active');document.getElementById('searchInput').placeholder=t==='bible'?'Rechercher dans la Bible...':'Demander à Meta AI ou rechercher';renderList()}
function doSearch(v){let items=document.querySelectorAll('.chat-item');items.forEach(it=>{it.style.display=it.textContent.toLowerCase().includes(v.toLowerCase())?'flex':'none'})}
function openChat(i){document.getElementById('mainContent').classList.add('hidden');document.querySelector('.tabs').classList.add('hidden');document.getElementById('chatView').classList.remove('hidden');document.getElementById('chatName').textContent=chats[i].n;document.getElementById('chatAvatar').src=chats[i].a;document.getElementById('messages').innerHTML=`<div style="background:#fff;padding:8px;border-radius:12px;margin:6px">Bonjour ${user.name} 🙏</div>`}
function backToList(){document.getElementById('chatView').classList.add('hidden');document.getElementById('settingsView').classList.add('hidden');document.getElementById('mainContent').classList.remove('hidden');document.querySelector('.tabs').classList.remove('hidden')}
function showSettings(){document.getElementById('mainContent').classList.add('hidden');document.querySelector('.tabs').classList.add('hidden');document.getElementById('settingsView').classList.remove('hidden')}
function togglePanel(){document.getElementById('emojiPanel').classList.toggle('hidden');document.getElementById('attachPanel').classList.add('hidden')}
function toggleAttach(){document.getElementById('attachPanel').classList.toggle('hidden');document.getElementById('emojiPanel').classList.add('hidden')}
let emojis=['😊','😂','❤️','🙏','😍','🔥','👍','🎉','😭','😇','🕊️','✨','📖','⛪','👏','💒','🌟','😀','😉','🤲','💐','🎵','😅','🥰','😁','👋','🙌','💪','😎','🤗','🌹','🕯️'];document.querySelector('#panelEmoji').innerHTML=emojis.map(e=>`<span onclick="insertEmoji('${e}')">${e}</span>`).join('');document.querySelector('#panelSticker .grid').innerHTML=['🙏','😇','❤️','🔥','🎉','⛪'].map(e=>`<span style="font-size:48px" onclick="sendSticker('${e}')">${e}</span>`).join('');document.querySelector('#panelGif').innerHTML=[1,2,3,4,5,6].map(i=>`<img src="https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif" style="width:80px;height:80px;object-fit:cover;border-radius:10px" onclick="sendGif()">`).join('');
function panelTab(t,btn){document.querySelectorAll('#emojiPanel button').forEach(b=>b.style.background='#f0f2f5');btn.style.background='#25D366';['panelEmoji','panelGif','panelSticker'].forEach(id=>document.getElementById(id).classList.add('hidden'));document.getElementById(t==='emoji'?'panelEmoji':t==='gif'?'panelGif':'panelSticker').classList.remove('hidden')}
function insertEmoji(e){document.getElementById('msgInput').value+=e;checkSend(document.getElementById('msgInput'))}
function sendSticker(e){addMsg(e);document.getElementById('emojiPanel').classList.add('hidden')}
function sendGif(){addMsg('🎞️ GIF envoyé');document.getElementById('emojiPanel').classList.add('hidden')}
function checkSend(inp){document.getElementById('micBtn').textContent=inp.value.trim()?'➤':'🎤'}
document.getElementById('msgInput').addEventListener('keydown',e=>{if(e.key==='Enter'){let v=e.target.value.trim();if(v){addMsg(v);e.target.value='';checkSend(e.target)}}});
function addMsg(t){let d=document.createElement('div');d.style.cssText='background:#d9fdd3;padding:8px;border-radius:12px;margin:6px 12px 6px auto;max-width:80%';d.textContent=t;document.getElementById('messages').appendChild(d)}
function sendPhoto(ev){let r=new FileReader();r.onload=()=>{let d=document.createElement('div');d.style.cssText='background:#d9fdd3;padding:8px;border-radius:12px;margin:6px 12px 6px auto';d.innerHTML=`<img src="${r.result}" style="width:180px;border-radius:10px">`;document.getElementById('messages').appendChild(d)};r.readAsDataURL(ev.target.files[0]);document.getElementById('attachPanel').classList.add('hidden')}
function shareLocation(){addMsg('📍 Localisation: Lubumbashi, Katanga, CD');document.getElementById('attachPanel').classList.add('hidden')}
function sendContact(){addMsg('👤 Contact partagé: '+user.name+' '+user.phone);document.getElementById('attachPanel').classList.add('hidden')}
function createPoll(){let q=prompt('Question du sondage:');if(q)addMsg('📊 Sondage: '+q)}
function createEvent(){let q=prompt('Nom événement:');if(q)addMsg('📅 Événement: '+q)}
let recTimer,recSec=0,paused=false;
function startVoice(){document.getElementById('recPanel').classList.remove('hidden');recSec=0;paused=false;recTimer=setInterval(()=>{if(!paused){recSec++;let m=Math.floor(recSec/60),s=recSec%60;document.getElementById('recTimer').textContent=m+':'+(s<10?'0':'')+s;document.getElementById('wave').textContent='.'.repeat(5+recSec%8)}},1000)}
function togglePause(){paused=!paused;document.getElementById('pauseBtn').textContent=paused?'▶️ Reprendre':'⏸️ Pause'}
function cancelVoice(){clearInterval(recTimer);document.getElementById('recPanel').classList.add('hidden')}
function sendVoice(){clearInterval(recTimer);document.getElementById('recPanel').classList.add('hidden');addMsg('🎤 Voice '+document.getElementById('recTimer').textContent)}
</script></body></html>
"""
 
components.html(HTML, height=850, scrolling=True)


