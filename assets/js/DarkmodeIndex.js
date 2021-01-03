let darkMode = localStorage.getItem('darkMode'); 
const darkModeToggle = document.querySelector('#DarkModeButton');

const enableDarkMode = () => {
  document.getElementById("StickyHeadline").classList.add("darkmode");
  document.body.classList.add('darkmode');
  document.body.classList.add('FontContrast');

  (function() {
    var titles = document.querySelectorAll(".left");
    var i = titles.length;
    while (i--) {
        titles[i].classList.add("LScrollDm")
    }
    })();
    (function() {
    var titles = document.querySelectorAll(".right");
    var i = titles.length;
    while (i--) {
        titles[i].classList.add("RScrollDm")
    }
    })();

  localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
  document.getElementById("StickyHeadline").classList.remove("darkmode");
  document.body.classList.remove('darkmode');
  document.body.classList.remove('FontContrast');

  (function() {
    var titles = document.querySelectorAll(".left");
    var i = titles.length;
    while (i--) {
        titles[i].classList.remove("LScrollDm")
    }
    })();
    (function() {
    var titles = document.querySelectorAll(".right");
    var i = titles.length;
    while (i--) {
        titles[i].classList.remove("RScrollDm")
    }
    })();

  localStorage.setItem('darkMode', null);
}
 
if (darkMode === 'enabled') {
  enableDarkMode();
}

darkModeToggle.addEventListener('click', () => {
  darkMode = localStorage.getItem('darkMode'); 
    
  if (darkMode !== 'enabled') {
    enableDarkMode();
  } else {  
    disableDarkMode(); 
  }
});