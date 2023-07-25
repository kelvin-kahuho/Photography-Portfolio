document.addEventListener('DOMContentLoaded', function() {
  const slider = document.querySelector('.carousel-slider');
  const slides = document.querySelectorAll('.carousel-slide');
  let slideIndex = 0;

  // Function to show the current slide
  function showSlide(index) {
    slider.style.transform = `translateX(-${index * 100}%)`;
  }

  // Function to handle the automatic slideshow
  function autoSlide() {
    slideIndex++;
    if (slideIndex >= slides.length) {
      slideIndex = 0;
    }
    showSlide(slideIndex);
  }

  // Start the automatic slideshow every 3 seconds (adjust the interval as needed)
  setInterval(autoSlide, 5000);
});
