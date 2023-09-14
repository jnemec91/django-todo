// JavaScript to rotate stickers in a carousel
const stickersContainer = document.getElementById('carousel-wrap');
const stickers = document.querySelectorAll('.slide');
const prevButton = document.getElementById('back');
const nextButton = document.getElementById('next');
let currentStickerIndex = 0;

function rotateToSticker(index) {
    window.scrollTo({ top: 0, behavior: 'smooth' })

    stickersContainer.style.transform = `translateX(-${index * 100}%)`;

}

prevButton.addEventListener('click', () => {
    currentStickerIndex = (currentStickerIndex - 1 + stickers.length) % stickers.length;
    rotateToSticker(currentStickerIndex);
});

nextButton.addEventListener('click', () => {
    currentStickerIndex = (currentStickerIndex + 1) % stickers.length;
    rotateToSticker(currentStickerIndex);
});