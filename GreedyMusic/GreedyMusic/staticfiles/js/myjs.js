$(document).ready(function(e){
    $('.search-panel .dropdown-menu').find('a').click(function(e) {
		e.preventDefault();
		var param = $(this).attr("value");
		//alert('param =' + param)
		var concept = $(this).text();
		$('.search-panel span#search_concept').text(concept);
		$('.input-group #search_param').val(param);
	});
});

function showdiv() {
	var disp = document.getElementById('add-form-container').style.display
	if(disp == "none")
	{
   		document.getElementById('add-form-container').style.display = "block";
   		$('html, body').animate({scrollTop: $("#add-form-container").offset().top}, 2000);
	}
   	if(disp == "block") 
   		document.getElementById('add-form-container').style.display = "none";
}

function doget()
{
	var url = document.getElementById("search_param").value;
	var search_term = document.getElementById("search_bar").value;
	var location = "/tracks/search/?q=all&search_term="+search_term;
	if(url != "") 
		location = url+search_term;
	window.location = location;
	return true;
}