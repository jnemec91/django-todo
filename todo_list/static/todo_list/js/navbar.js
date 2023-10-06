

function ToggleMenu(){
    let navbar = document.getElementById("navbar");
    let navbar_toggler = document.getElementById("navbar-toggler");
    
    navbar.classList.toggle('collapsed');
    navbar_toggler.classList.toggle('toggler-active');
}