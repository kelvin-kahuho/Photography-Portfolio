// Function to switch between categories
function switchCategory(categoryIndex) {
    const carousels = document.getElementsByClassName('carousel');
    const buttons = document.getElementsByTagName('button');
  
    // Hide all carousels and remove active class from buttons
    for (let i = 0; i < carousels.length; i++) {
      carousels[i].style.display = 'none';
      buttons[i].classList.remove('active');
    }
  
    // Show the selected carousel and add active class to the corresponding button
    carousels[categoryIndex - 1].style.display = 'block';
    buttons[categoryIndex - 1].classList.add('active');
  }
  