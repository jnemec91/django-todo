function showModal(id, wrap) {
    document.getElementById(wrap).classList.add("wrap-active");
    document.getElementById(id).classList.add("active");
}

function hideModal(id, wrap) {
    document.getElementById(wrap).classList.remove("wrap-active");
    document.getElementById(id).classList.remove("active");
}

function copyToClipboard(id) {
    var copyText = document.getElementById(id);
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
}