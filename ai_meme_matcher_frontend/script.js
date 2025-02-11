const fileNameDisplay = document.getElementById("file-name");
const memeBtn = document.querySelector("#uploadButton");
const uplaodBtn = document.querySelector(".file-upload");
const fileInput = document.getElementById("fileInput");
const selectedImage = document.getElementById("selectedImage");
const uploadButton = document.getElementById("uploadButton");
const matchedMeme = document.getElementById("matchedMeme");

// const api_url = "{{API_URL}}";
const api_url = "https://meme-matcher.onrender.com/match";

// Preload all slideshow images
const slideshowImages = 53;
const preloadedImages = [];

function preloadImages() {
  for (let i = 1; i <= slideshowImages; i++) {
    const img = new Image();
    img.src = `memes/${i}.png`;
    preloadedImages.push(img);
  }
}

// Call the preload function when the page loads
window.onload = preloadImages;

fileInput.addEventListener("change", function (event) {
  const file = event.target.files[0];

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      selectedImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

uploadButton.addEventListener("click", function () {
  if (fileInput.files.length === 0) {
    alert("Please select an image file.");
    return;
  }

  let currentSlide = 1;
  let slideshowInterval;

  // Start the slideshow using preloaded images
  slideshowInterval = setInterval(() => {
    matchedMeme.src = preloadedImages[currentSlide - 1].src;
    currentSlide = currentSlide + 1;
    if (currentSlide == slideshowImages + 1) currentSlide = 1;
  }, 100);

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  fetch(api_url, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      clearInterval(slideshowInterval);

      if (data.matched_meme) {
        confettiFun();
        matchedMeme.src = `memes/${data.matched_meme}`;
        uplaodBtn.style.display = "";
        memeBtn.style.display = "none";
      } else if (data.error) {
        alert(data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while processing your request. " + error);
      clearInterval(slideshowInterval);
    });
});

fileInput.addEventListener("change", function (event) {
  const file = event.target.files[0];

  uplaodBtn.style.display = "none";
  memeBtn.style.display = "";
});

const confettiFun = () => {
  var scalar = 2;
  var unicorn = confetti.shapeFromText({ text: "😂", scalar });

  var defaults = {
    spread: 360,
    ticks: 100,
    gravity: 0,
    decay: 0.96,
    startVelocity: 15,
    shapes: [unicorn],
    scalar,
  };

  function shoot() {
    confetti({
      ...defaults,
      particleCount: 30,
    });

    confetti({
      ...defaults,
      particleCount: 5,
      flat: true,
    });

    confetti({
      ...defaults,
      particleCount: 15,
      scalar: scalar / 2,
      shapes: ["circle"],
    });
  }

  setTimeout(shoot, 0);
  setTimeout(shoot, 300);
  setTimeout(shoot, 500);
};
