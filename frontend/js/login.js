// Background slider
const slides = document.querySelectorAll(".slide");
let index = 0;

setInterval(() => {
  slides[index].classList.remove("active");
  index = (index + 1) % slides.length;
  slides[index].classList.add("active");
}, 3500);

// Login handler placeholder
document.getElementById("loginForm").addEventListener("submit", e => {
  e.preventDefault();
  alert("Login submitted");
});
