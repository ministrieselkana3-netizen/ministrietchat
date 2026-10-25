/* EL KANA MINISTRIES TCHAT — Interactions principales */
 
"use strict";
 
document.addEventListener("DOMContentLoaded", function () {
    initialiserNavigation();
    initialiserMessagerieDemo();
    initialiserRecherche();
});
 
/* Navigation entre les rubriques */
function initialiserNavigation() {
    const boutons = document.querySelectorAll("[data-page]");
    const pages = document.querySelectorAll(".page");
 
    boutons.forEach(function (bouton) {
        bouton.addEventListener("click", function () {
            const cible = bouton.getAttribute("data-page");
            const pageCible = document.getElementById(cible);
 
            if (!pageCible) {
                console.warn("Rubrique introuvable :", cible);
                return;
            }
 
            pages.forEach(function (page) {
                page.classList.remove("active");
            });
 
            boutons.forEach(function (element) {
                element.classList.remove("active");
            });
 
            pageCible.classList.add("active");
            bouton.classList.add("active");
 
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    });
}
 
/* Démonstration locale de la messagerie */
function initialiserMessagerieDemo() {
    const formulaire = document.getElementById("form-message");
    const champ = document.getElementById("message");
    const liste = document.getElementById("liste-messages");
 
    if (!formulaire || !champ || !liste) {
        return;
    }
 
    formulaire.addEventListener("submit", function (evenement) {
        evenement.preventDefault();
 
        const texte = champ.value.trim();
 
        if (!texte) {
            return;
        }
 
        const message = document.createElement("div");
        message.className = "card message-local";
 
        const contenu = document.createElement("p");
        contenu.textContent = texte;
 
        const indication = document.createElement("small");
        indication.textContent = "Message de démonstration — enregistré uniquement sur cette page.";
 
        message.appendChild(contenu);
        message.appendChild(indication);
        liste.appendChild(message);
 
        champ.value = "";
        champ.focus();
    });
}
 
/* Recherche simple dans les cartes visibles */
function initialiserRecherche() {
    const recherche = document.getElementById("recherche");
    const cartes = document.querySelectorAll(".card");
 
    if (!recherche) {
        return;
    }
 
    recherche.addEventListener("input", function () {
        const terme = recherche.value.trim().toLowerCase();
 
        cartes.forEach(function (carte) {
            const correspond = carte.textContent.toLowerCase().includes(terme);
            carte.hidden = terme !== "" && !correspond;
        });
    });
}

if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("./service-worker.js")
      .catch(function (error) {
        console.error("Erreur du service worker :", error);
      });
  });
}
