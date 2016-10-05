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

          i = 0;
          result.forEach(
            function(morpheme){
              surface = morpheme[0];
              unidic_id = morpheme[1];
              morph_type = morpheme[2];
              btn_type = "btn-default";
              if (morph_type == "easy"){
                btn_type = "btn-primary";
              }
              id_morph = "morph_" + i;
              morph = $(
                '<button type="button" class="btn ' + btn_type + '" unidic_id="' + unidic_id + '" morph_type="' + morph_type + '" id="' + id_morph + '">' + morpheme[0] +'</button>'
              ).appendTo("#textarea2 div");

              id_morph = "#" + id_morph;
              morph = $(id_morph);
              morph.click(function(){
                $.ajax({
                  type: "POST",
                  url: "/api/check_easy",
                  data:  JSON.stringify({
                    "unidic_id": morph.attr("unidic_id"),
                    "surface": morph.val()
                  }),
                  contentType: 'application/JSON',
                  dataType : 'JSON',
                  scriptCharset: 'utf-8',
                  success: function(res){
                    console.log(id_morph);
                    console.log(res);
                    $(id_morph).removeClass("btn-default");
                    $(id_morph).removeClass("btn-primary");
                    if (res == "none"){
                      $(morph).addClass("btn-default");
                    } else{
                      $(id_morph).addClass("btn-primary");
                    }
                  },
                  error: function(xhr, status, err) {
                    console.log("error");
                    console.log(status);
                    console.log(err);
                  }
                });
              });
              // btn-primary:やさしい日本語
              // btn-Danger:
              // btn-default:
            i += 1;
          });
          // $("#textarea2 div").text(result);
        },

        error: function(xhr, status, err) {
          console.log("error");
        }
      });
    }
  }
}

// attr("morph_type")
