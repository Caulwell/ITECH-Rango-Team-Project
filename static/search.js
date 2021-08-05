const searchBar = document.getElementById("searchBar");
const results = document.getElementById("search-results");
const elements = results.getElementsByTagName("li");


searchBar.addEventListener("keyup", e => {
    const searchString = e.target.value.toUpperCase();

    if(searchString == ""){
        results.classList.add("d-none");
    } else {
        results.classList.remove("d-none");

        for(i = 0; i < elements.length; i++){
            a = elements[i].getElementsByTagName("a")[0];
            txtValue = a.textContent || a.innerText;
            if(txtValue.toUpperCase().indexOf(searchString) > -1){
                elements[i].style.display = "";
            } else {
                elements[i].style.display = "none";
            }
        }
    }

});

searchBar.addEventListener("focusout", e=> {
    results.classList.add("d-none");
});

searchBar.addEventListener("focusin", e=> {
    results.classList.remove("d-none");
});