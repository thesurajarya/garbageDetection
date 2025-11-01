const whatsappNumber = "91xxxxxxxxxx";
const message = encodeURIComponent("Hello, I want to report waste.");
document.getElementById("whatsappLink").href = `https://wa.me/${whatsappNumber}?text=${message}`;
