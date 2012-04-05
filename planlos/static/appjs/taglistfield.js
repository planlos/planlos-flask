function ajax_get_tag(inst){
    $.get("/termine/tags/"+$(this).val(),
	  function(data) {
	      //$(".taglist")
	  }
	 );
}

function remove_tag(){
    var rtag = $(this).attr('tagval');
    $(".taglistcontainer > p").remove(":contains('"+rtag+"')");
    return false;
}

function remove_tag2(val){
    $("#taglist > div").remove(":contains('"+val+"')");
    return false;
}

function add_tag(inst){
    var ntag = $(".tagadder").val();
    if (ntag == '') return false;
    $(".taglistcontainer").append("<p><span>"+ntag+"</span><a class=\"removetag\" tagval=\""+ntag+"\" href=\"\">(-)</a></p>");
    $(".removetag").click( remove_tag );
    $(".tagadder").attr({value:""});
    return false;
}

