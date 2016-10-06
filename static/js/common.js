$(function() {
  display_number_of_easy_japanese_in_database();
});

function display_number_of_easy_japanese_in_database(){
  $.ajax({
    type: "GET",
    url: "api/easy_morph_count",
    contentType: 'application/JSON',
    dataType : 'JSON',
    scriptCharset: 'utf-8',

    success: function(result){
      $("#number_of_words").html(result);
    },

    error: function(xhr, status, err) {
      console.log("error");
    }
  });
}
