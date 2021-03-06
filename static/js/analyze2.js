// リアルタイムキー入力を獲得
$(function() {
  $("#input_sentence").each(function(){
    $(this).bind('keyup', hoge(this));
  });
});
// リアルタイムキー入力に発火する関数
function hoge(elm){
  var v, old = elm.value;
  return function(){
    if(old != (v=elm.value)){
      old = v;
      str = $(this).val();
      // $("#textarea div").text(str);
      $.ajax({
        type: "GET",
        url: "api/tokenize_2",
        data: {
          "input_text": str
        },
        contentType: 'application/JSON',
        dataType : 'JSON',
        scriptCharset: 'utf-8',

        success: function(result){
          // テキストエリアを初期化
          $("#textarea div").html("");
          text = "";

          for(var index in result){
            // 要素の獲得
            morpheme = result[index]
            surface = morpheme[0];
            unidic_id = morpheme[1];
            morph_type = morpheme[2];

            // ボタンのタイプ
            btn_type = "btn-default";
            if (morph_type == "easy"){
              btn_type = "btn-primary";
            } else if (morph_type == "unk") {
              btn_type = "btn-warning";
            }
            // ボタンのID
            id_morph = "morph_" + index;
            // ボタン生成
            morph = $(
              '<button type="button" class="btn ' + btn_type + '" unidic_id="' + unidic_id + '" morph_type="' + morph_type + '" id="' + id_morph + '">' + morpheme[0] +'</button>'
            ).appendTo("#textarea div");
            id_morph = "#" + id_morph;
            // ボタンに機能を付ける

            $(id_morph).click(function(){
              im = this;
              $.ajax({
                type: "POST",
                url: "api/check_easy_2",
                data:  JSON.stringify({
                  "unidic_id": $(im).attr("unidic_id"),
                  "surface": $(im).text()
                }),
                contentType: 'application/JSON',
                dataType : 'JSON',
                scriptCharset: 'utf-8',

                success: function(res){
                  $(im).removeClass("btn-default");
                  $(im).removeClass("btn-primary");
                  if (res == "none"){
                    $(im).addClass("btn-default");
                  } else{
                    $(im).addClass("btn-primary");
                  }
                  display_number_of_easy_japanese_in_database();
                },

                error: function(xhr, status, err) {
                  console.log("error");
                  console.log(status);
                  console.log(err);
                }
              });
            });
          }
          display_number_of_easy_japanese_in_database();
        },

        error: function(xhr, status, err) {
          console.log("error");
        }
      });
    }
  }
}
