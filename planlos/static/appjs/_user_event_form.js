function ajax_by_date(inst){
    var s = $(this).val().split("-").join("/");
    $.get("/termine/"+s+"/",
	  function(data) {
	      $(".events_by_date").replaceWith(data);
	  } 
	 );
}


function ajax_get_tag(inst){
    $.get("/termine/tags/"+$(this).val(),
	  function(data) {
	      //$(".taglist")
	  }
	 );
}

function get_media_file_with_id(id, filename, responseJSON)
{
    $.get("/termine/media/"+responseJSON.id, function(data) {
	      // render return html
	      // add id into form
	      $(".flyerupload").append(data);
	      // <input type="text" name="flyer" value="http://bla.de/" id="id_url" />
	      $("#hidden-media-fields").append("<p><span>"+responseJSON.id+"</span></p>");
	  }
	 );
}

function listProperties(obj) {
   var propList = "";
   for(var propName in obj) {
      if(typeof(obj[propName]) != "undefined") {
         propList += (propName + ", ");
      }
   }
   alert(propList);
}


function remove_tag(){
    var rtag = $(this).attr('tagval');
    $(".taglistcontainer > p").remove(":contains('"+rtag+"')");
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

function user_form_submit(inst)
{
    // Tags in Form einfuegen
    var ntags = [];
    $(".taglistcontainer > p").each( function (idx ) {
					 //alert( $(this).find('span').text() );
					 ntags.push($(this).find('span').text());
				     } );
    var tagvalue = ntags.join(",");
    $("#tags").attr({value: tagvalue});
    // Bild Referenzen
    
    //var flyerref = [];
    //$("#hidden-media-fields > p").each( function (idx ) {
//					    alert( $(this).find('span').text() );
//					    flyerref.push($(this).find('span').text());
//				     } );
  //  var flyerref_input = flyerref.join(",");
   // $(".flyerreflist").attr({value: flyerref_input});
}

function get_events_by_date(inst){
    var s = $(this).val().split("-").join("/");
    $.get("/webservice/events/"+s,
	  function(data) {
	      $(".events_by_date").replaceWith(data);
	  } 
	 );
}



$(document).ready(
    function() {
	$(".tagadder").autocomplete( { source: "/webservice/tags/"} );
	// Tags
        $( "button", ".tagform" ).button();
        $( "button", ".tagform" ).click(add_tag);
        $(".removetag").click( remove_tag );
        $( "button", "#id_flyer" ).button();
	$(".userform").submit( user_form_submit );
	$(".eventdate_picker").change( get_events_by_date );
	$(".eventdate_picker").datepicker( {dateFormat: "yy-mm-dd" } );
	var time_suggestions = ['00:00', '00:15', '00:30', '00:45', '01:00', '01:15', '01:30', '01:45', '02:00', '02:15', '02:30', '02:45', '03:00', '03:15', '03:30', '03:45', '04:00', '04:15', '04:30', '04:45', '05:00', '05:15', '05:30', '05:45', '06:00', '06:15', '06:30', '06:45', '07:00', '07:15', '07:30', '07:45', '08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30', '11:45', '12:00', '12:15', '12:30', '12:45', '13:00', '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30', '17:45', '18:00', '18:15', '18:30', '18:45', '19:00', '19:15', '19:30', '19:45', '20:00', '20:15', '20:30', '20:45', '21:00', '21:15', '21:30', '21:45', '22:00', '22:15', '22:30', '22:45', '23:00', '23:15', '23:30', '23:45'];
	$(".eventtime_picker").autocomplete( {source: time_suggestions} );
        $("#location").autocomplete( { source: "/webservice/locations/"} );
	$("#timeperiod").attr('readonly', 'readonly');
	$("#dateperiod").attr('readonly', 'readonly');
	$("#dateperiod").datepicker("disable");
	$("#buttonperiod").button()
	$("#buttonperiod").click( function() {
	    if ( $("#timeperiod").attr('readonly') == 'readonly' )
	    {
		// enable
		$("#timeperiod").removeAttr('readonly');
		$("#dateperiod").removeAttr('readonly');
		$("#dateperiod").datepicker("enable");
		//$(this).text("bis")
	    }
	    else
	    {
		//disable
		$("#timeperiod").attr('readonly', 'readonly');
		$("#dateperiod").attr('readonly', 'readonly');
		$("#timeperiod").val(null);
		$("#dateperiod").val(null);
		$("#dateperiod").datepicker("disable");
		//$(this).text("...")
	    }
	    return false;
	});
	
    }
);
