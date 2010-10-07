function toggle(d) {
if(d.length < 1) { return; }
if(document.getElementById(d).style.display == "none") 
    { document.getElementById(d).style.display = "inline"; }
else { document.getElementById(d).style.display = "none"; }
}

