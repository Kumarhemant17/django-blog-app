// Toggle menu
function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.classList.toggle("show");
}

// Close menu when clicking outside
document.addEventListener("click", function(event) {
    const menu = document.getElementById("menu");
    const button = document.querySelector(".menu-btn");

    if (!button.contains(event.target) && !menu.contains(event.target)) {
        menu.classList.remove("show");
    }
});