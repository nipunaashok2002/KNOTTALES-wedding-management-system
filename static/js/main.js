/* ==========================================================
   KnotTales — Global JavaScript
   Handles: background-image loaders, fade animations, helpers
   Author: Nipuna's Theme
   ========================================================== */

/* ------------------------------
   1. BACKGROUND IMAGE LOADER
   Elements use: data-img="path/to/image.jpg"
   ------------------------------ */
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-img]").forEach((el) => {
        const img = el.dataset.img;
        if (img && img.trim() !== "") {
            el.style.backgroundImage = `url('${img}')`;
            el.style.backgroundSize = "cover";
            el.style.backgroundPosition = "center";
            el.style.backgroundRepeat = "no-repeat";
        }
    });
});

/* ------------------------------
   2. FADE-IN ON SCROLL
   Matches .fade-in CSS class
   ------------------------------ */
const fadeEls = document.querySelectorAll(".fade-in");

function revealOnScroll() {
    const triggerPoint = window.innerHeight * 0.88;

    fadeEls.forEach((el) => {
        const top = el.getBoundingClientRect().top;
        if (top < triggerPoint) {
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
        }
    });
}

window.addEventListener("scroll", revealOnScroll);
window.addEventListener("load", revealOnScroll);

/* ------------------------------
   3. HEART BUTTON (Save Vendor)
   Used in vendors.html
   ------------------------------ */
document.addEventListener("click", (e) => {
    if (e.target.closest(".heart-btn")) {
        const btn = e.target.closest(".heart-btn");
        btn.classList.toggle("active");

        btn.innerHTML = btn.classList.contains("active")
            ? '<i class="fas fa-heart"></i>'
            : '<i class="far fa-heart"></i>';
    }
});

/* ------------------------------
   4. CHECKLIST INTERACTION
   Used in planning.html
   ------------------------------ */
function toggleTask(checkbox) {
    const item = checkbox.parentElement;
    if (checkbox.checked) item.classList.add("completed");
    else item.classList.remove("completed");
}

/* Make function available globally */
window.toggleTask = toggleTask;

/* ------------------------------
   5. OPTIONAL SMOOTH SCROLL
   For anchor links like #pricing
   ------------------------------ */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: "smooth" });
        }
    });
});
