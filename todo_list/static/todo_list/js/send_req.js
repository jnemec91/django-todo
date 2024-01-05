function send_req(url){
    const request = new XMLHttpRequest();

    csfr_token = document.getElementsByName('csrfmiddlewaretoken')[0].value

    request.onreadystatechange = function() {
        if (request.readyState == XMLHttpRequest.DONE) {
            if( request.status == 200 && request.responseText == "reload"){
                location.reload();
            }
        }
    }

    request.open("POST", url);
    request.setRequestHeader("X-CSRFToken", csfr_token); 
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");     
    request.send();
}