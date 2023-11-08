document.addEventListener("DOMContentLoaded", function() {
    var loader = document.querySelector(".loader");
    var content = document.querySelector(".content");

    setTimeout(function() {
        loader.style.display = "none";
        content.style.display = "block";
    }, 2000); // Attends 2 secondes avant d'afficher le contenu
});
