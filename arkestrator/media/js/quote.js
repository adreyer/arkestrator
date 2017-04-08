function createInstance() {
    req = new XMLHttpRequest();
    return(req);
}

function quote(url) { 
    var req = createInstance();
    var quotation = document.getElementById('id_body').value;
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            if (req.status == 200) {
                quotation = quotation + req.responseText
                document.getElementById('id_body').value = quotation;
            } else {
                document.getElementById('id_body').value="Error: status " + req.status + " " + req.statusText;
            }
        }
    }
    req.open("GET", url, true);
    req.send(null);
}
