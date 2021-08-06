let ratingDivs = $(".review-item");


for(let i=0; i < ratingDivs.length; i++){
    let rating_div = ratingDivs[i].getElementsByClassName("rating-div")[0];

    let p = rating_div.getElementsByTagName("p")[0];

    let rating = parseInt(p.innerHTML);

    p.remove();

    let filledStar = '<span style="color:#007bff" class="fa fa-star checked"></span>';

    let div = document.createElement("div");

    for(let j=0; j<rating; j++){
        div.innerHTML += filledStar;
    }

    rating_div.append(div);
    

}


function show_update_url() {
    document.getElementById("update_url").style.display = "block";

}
function hide_update_url() {
    document.getElementById("update_url").style.display = "none";

}
function show_update_pic() {
    document.getElementById("update_pic").style.display = "block";

}
function hide_update_pic() {
    document.getElementById("update_pic").style.display = "none";

}


