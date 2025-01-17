function send_req(url, method){
    const request = new XMLHttpRequest();

    csfr_token = document.getElementsByName('csrfmiddlewaretoken')[0].value

    request.onreadystatechange = function() {
        if (request.readyState == XMLHttpRequest.DONE) {
            if( request.status == 200 && request.responseText == "reload"){
                location.reload();
            }

            else if(request.status == 200){
                console.log(request.responseText);
                return request.responseText;
            }
        }
    }

    request.open(method, url);
    request.setRequestHeader("X-CSRFToken", csfr_token); 
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");     
    request.send();
}