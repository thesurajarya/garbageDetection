const whatsappNumber = "91xxxxxxxxxx"; // India country code assumed. Update number.
const predefinedText = encodeURIComponent("I want to report waste");
const whatsappURL = `https://wa.me/${whatsappNumber}?text=${predefinedText}`;

document.getElementById("whatsappLink").href = whatsappURL;
