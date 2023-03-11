function PageLoaded(){
    console.log("Page Loaded");

}


function UpdateSemaboxList(){
    console.log("Update Semabox List");

}






// #### API #### //
function APISemaboxGetAll(){
    console.log("API Semabox Get All");
    var semaboxList = [];
    
    var xhttp = new XMLHttpRequest();
    xhttp.oneradystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { // if request is successfull and status OK
            semaboxList = JSON.parse(this.responseText);
        }
    }
    xhttp.open("GET", "/api/manage-semabox/getAll", false); // false = synchrone
    xhttp.send();

    console.log(semaboxList);
    return semaboxList;
}