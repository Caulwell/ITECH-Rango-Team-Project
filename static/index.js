let ratingDivs = document.getElementsByClassName("rating");

// setTimeout(function(){
    
// }, 500);

for(let i=0; i < ratingDivs.length; i++){
    let p = ratingDivs[i].getElementsByTagName("p")[0];

    let rating = parseInt(p.innerHTML);

    p.remove();
    let filledStar = '<span style="color:#007bff" class="fa fa-star checked"></span>';

    let div = document.createElement("div");

    for(let j=0; j<rating; j++){
        div.innerHTML += filledStar;
    }

    ratingDivs[i].appendChild(div);
    

}