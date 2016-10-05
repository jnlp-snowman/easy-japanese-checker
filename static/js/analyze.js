var r;
$(function() {
  $("#textarea2 textarea").each(function(){
    $(this).bind('keyup', hoge(this));
  });
});

function writeTable(result)
{
  $("#tbl-result tbody").html("");
  result.forEach(
    function(elem){
      $(
        "<tr>" +
        "<td>" + elem[0] + "</td>" +
        "<td>" + elem[1] + "</td>" +
        "</tr>"
      ).appendTo("#tbl-result tbody");
    }
  );
}

function hoge(elm){
  var v, old = elm.value;
  return function(){
    if(old != (v=elm.value)){
      old = v;
      str = $(this).val();
      // $("#textarea2 div").text(str);
      $.ajax({
        type: "GET",
        url: "/api/tokenize",
        data: {
          "input_text": str
        },
        contentType: 'application/JSON',
        dataType : 'JSON',
        scriptCharset: 'utf-8',

        success: function(result){
          //console.log("success");
          console.log(result);
          $("#textarea2 div").html("");
          text = "";
          result.forEach(
            function(morpheme){
              surface = morpheme[0]
              unidic_id = morpheme[1]
              $(
                '<button type="button" class="btn btn-default">' + morpheme[0] +'</button>'
              ).appendTo("#textarea2 div")
            }
          );
          // $("#textarea2 div").text(result);
        },

        error: function(xhr, status, err) {
          //console.log("error");
        }
      });
    }
  }
}
