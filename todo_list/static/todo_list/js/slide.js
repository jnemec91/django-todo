// JavaScript to rotate stickers in a carousel
const stickersContainer = document.getElementById('carousel-wrap');
const stickers = document.querySelectorAll('.slide');
const prevButton = document.getElementById('back');
const nextButton = document.getElementById('next');
let currentStickerIndex = 0;

function getRange(id, number){
    let range = [];
    for (let i = id; i < number; i++){
        range.push(i);
    }
    return range;

}

function rotateToSticker(index) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    stickersContainer.style.transform = `translateX(-${index * 100}%)`;

}

function quickRotate(index) {
    currentStickerIndex = index;
    stickersContainer.style.transform = `translateX(-${index * 100}%)`;
    setRB(index);
}

function setRB(id){
    let rbs = document.querySelectorAll('.round-button');

    rbs.forEach(rb => {
        rb.classList.remove('rb-active');
        rb.classList.add('inisible_rb');

        let rbv = parseInt(rb.value);
        
        let plusnum = id+3
        let minusnum = id-2

        if (plusnum > stickers.length){
            minusnum = minusnum - (plusnum-(stickers.length));
        }

        if (minusnum < 0){
            plusnum = plusnum + Math.abs(minusnum);
        }

        let plusrange = getRange(id , plusnum);
        let minusrange = getRange(minusnum, id);
        
        if (plusrange.includes(rbv) || minusrange.includes(rbv)){
            rb.classList.remove('inisible_rb');
        }

    });

    let rb = document.getElementById('rb_'+id);
    rb.classList.add('rb-active');
}


prevButton.addEventListener('click', () => {
    currentStickerIndex = (currentStickerIndex - 1 + stickers.length) % stickers.length;
    setRB(currentStickerIndex);
    rotateToSticker(currentStickerIndex);
});

nextButton.addEventListener('click', () => {
    currentStickerIndex = (currentStickerIndex + 1) % stickers.length;
    setRB(currentStickerIndex);
    rotateToSticker(currentStickerIndex);
});