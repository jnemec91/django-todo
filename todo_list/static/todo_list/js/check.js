function check_task(url){
    const request = new XMLHttpRequest();

    csfr_token = document.getElementsByName('csrfmiddlewaretoken')[0].value

    request.open("POST", url);
    request.setRequestHeader("X-CSRFToken", csfr_token); 
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");     
    request.send();
}