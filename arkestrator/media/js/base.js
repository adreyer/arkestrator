function toggle(d) {
if(d.length < 1) { return; }
if(document.getElementById(d).style.display == "none") 
    { document.getElementById(d).style.display = "inline"; }
else { document.getElementById(d).style.display = "none"; }
}


function fill_field(field, newtext, append) {
    var contents='';
    if (append) {
        var contents=document.getElementById(field).value
    }
    document.getElementById(field).value = contents + newtext;
}
