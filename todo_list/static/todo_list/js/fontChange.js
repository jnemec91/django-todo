'use strict'

const fontSelect = document.getElementById('font_style');

fontSelect.addEventListener('change', function() {
    // Get the selected font
    const font = fontSelect.options[fontSelect.selectedIndex].text;
    fontSelect.style.fontFamily = font;
});