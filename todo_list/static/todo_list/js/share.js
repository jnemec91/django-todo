function showShareModal(id) {
    document.getElementById('share-modal-wrap').classList.add("active");
    document.getElementById(id).classList.add("active");
}

function hideShareModal(id) {
    document.getElementById('share-modal-wrap').classList.remove("active");
    document.getElementById(id).classList.remove("active");
}

function copyToClipboard(id) {
    var copyText = document.getElementById(id);
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
}