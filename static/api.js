// #### API #### //
function APISemaboxGetAll(){
    console.log("API Semabox Get All");
    var semaboxList = [];
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            semaboxList = JSON.parse(this.responseText);
            console.log("API Semabox Get All"+semaboxList);
        }
    };
    xhttp.open("GET", "/api/manage-semabox/getAll", false); // false = synchrone
    xhttp.send();

    return semaboxList;
}