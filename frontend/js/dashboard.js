// Sample interaction mock. Replace later with backend fetch & Leaflet.
const mapModal = document.getElementById("mapPopup");
const closeBtn = document.getElementById("closeMap");

document.querySelectorAll(".map-btn").forEach(btn => {
  btn.onclick = () => {
    mapModal.style.display = "flex";
    document.getElementById("map").innerHTML = "<p style='padding:20px'>Map loads here</p>";
  };
});

closeBtn.onclick = () => mapModal.style.display = "none";
window.onclick = e => { if(e.target == mapModal) mapModal.style.display = "none"; }
