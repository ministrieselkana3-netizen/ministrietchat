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

// Enregistrement de messages audio (aperçu sur cet appareil)
document.addEventListener("DOMContentLoaded", function () {
  const demarrer = document.getElementById("demarrer-audio");
  const arreter = document.getElementById("arreter-audio");
  const etat = document.getElementById("etat-audio");
  const apercu = document.getElementById("apercu-audio");

  if (!demarrer || !arreter || !etat || !apercu) return;

  let enregistreur = null;
  let morceaux = [];

  demarrer.addEventListener("click", async function () {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia ||
        typeof MediaRecorder === "undefined") {
      etat.textContent =
        "Ce navigateur ne permet pas l’enregistrement audio. Essaie une version récente de Chrome.";
      return;
    }

    try {
      const flux = await navigator.mediaDevices.getUserMedia({ audio: true });
      morceaux = [];
      enregistreur = new MediaRecorder(flux);

      enregistreur.addEventListener("dataavailable", function (evenement) {
        if (evenement.data && evenement.data.size > 0) {
          morceaux.push(evenement.data);
        }
      });

      enregistreur.addEventListener("stop", function () {
        const blob = new Blob(morceaux, {
          type: enregistreur.mimeType || "audio/webm"
        });
        const url = URL.createObjectURL(blob);

        const lecteur = document.createElement("audio");
        lecteur.controls = true;
        lecteur.src = url;
        lecteur.setAttribute("aria-label", "Écouter le message audio enregistré");

        const telecharger = document.createElement("a");
        telecharger.href = url;
        telecharger.download = "message-audio.webm";
        telecharger.textContent = "Télécharger l’audio";
        telecharger.style.display = "inline-block";
        telecharger.style.marginTop = "8px";

        const bloc = document.createElement("div");
        bloc.className = "card";
        bloc.appendChild(lecteur);
        bloc.appendChild(telecharger);
        apercu.prepend(bloc);

        etat.textContent =
          "Enregistrement terminé. Tu peux écouter ou télécharger cet audio.";
        flux.getTracks().forEach(function (piste) {
          piste.stop();
        });
      });

      enregistreur.start();
      demarrer.disabled = true;
      arreter.disabled = false;
      etat.textContent = "Enregistrement en cours… Parle dans le microphone.";
    } catch (erreur) {
      etat.textContent =
        "Accès au microphone refusé ou indisponible. Autorise le microphone dans le navigateur et réessaie.";
      console.error("Erreur du microphone :", erreur);
    }
  });

  arreter.addEventListener("click", function () {
    if (enregistreur && enregistreur.state !== "inactive") {
      enregistreur.stop();
      demarrer.disabled = false;
      arreter.disabled = true;
    }
  });
});
