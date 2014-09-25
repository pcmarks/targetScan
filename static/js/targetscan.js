/**
 * Created with IntelliJ IDEA.
 * User: pcmarks
 * Date: 2/20/14
 * Time: 10:19 AM
 * To change this template use File | Settings | File Templates.
 */


function copyToClipboard(text) {

    window.prompt("Copy to clipboard: Ctrl-C, Enter", text);
}

function downloadResults() {
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("GET", "download/all");
    xmlhttp.send();
}