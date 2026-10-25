"use strict";
 
document.addEventListener("DOMContentLoaded", function () {
    // Navigation entre les rubriques
    const boutons = document.querySelectorAll("[data-page]");
    const pages = document.querySelectorAll(".page");
 
    boutons.forEach(function (bouton) {
        bouton.addEventListener("click", function () {
            const cible = bouton.getAttribute("data-page");
            const pageCible = document.getElementById(cible);
 
            if (!pageCible) {
                console.error("Rubrique introuvable :", cible);
                return;
            }
 
            pages.forEach(function (page) {
                page.classList.remove("active");
                page.hidden = true;
            });
 
            boutons.forEach(function (element) {
                element.classList.remove("active");
            });
 
            pageCible.hidden = false;
            pageCible.classList.add("active");
            bouton.classList.add("active");
 
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    });
 
    // Messages de démonstration
    const formulaire = document.getElementById("form-message");
    const champ = document.getElementById("message");
    const liste = document.getElementById("liste-messages");
 
    if (formulaire && champ && liste) {
        formulaire.addEventListener("submit", function (evenement) {
            evenement.preventDefault();
            const texte = champ.value.trim();
            if (!texte) return;
 
            const message = document.createElement("div");
            message.className = "card message-local";
 
            const contenu = document.createElement("p");
            contenu.textContent = texte;
            message.appendChild(contenu);
            liste.appendChild(message);
 
            champ.value = "";
            champ.focus();
        });
    }
 
    // Recherche dans la page
    const recherche = document.getElementById("recherche");
 
    if (recherche) {
        recherche.addEventListener("input", function () {
            const terme = recherche.value.trim().toLowerCase();
            const cartes = document.querySelectorAll(".card");
 
            cartes.forEach(function (carte) {
                carte.hidden = terme !== "" &&
                    !carte.textContent.toLowerCase().includes(terme);
            });
        });
    }
});
