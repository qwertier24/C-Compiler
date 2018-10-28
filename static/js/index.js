$(function() {
  $("#run").click(function() {
    $.ajax({
      url: "/run/",
      type: "post",
      data: {
        "input":$("#input").val(),
        "codes":$("#codes").val()
      },
      success : function(data){
        if(data["verdict"] == "success") {
          $("#output").val(data["output"]);
        } else {
          alert(data["message"]);
        }
      },
      error : function(data) {
        alert("网站错误，请联系管理员");
      }
    });
  });
  $("#compile").click(function() {
    $.ajax({
      url: "/compile/",
      type: "post",
      data: {
        "codes":$("#codes").val()
      },
      success : function(data){
        if(data["verdict"] == "success") {
          $("#output").val(data["output"]);
        } else {
          alert(data["message"]);
        }
      },
      error : function(data) {
        alert("网站错误，请联系管理员");
      }
    });
  });
});
