/**
 * Created by YangQ on 2017/9/5.
 */

function sendurl(){
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
    var urlinfo = $("#urlinfo").val();
    if (urlinfo == "")
        {
        }
    else
        {
        xmlhttp.open("GET",urlinfo,true);
        xmlhttp.send();
        xmlhttp.onreadystatechange=function()
            {
            if (xmlhttp.readyState==4 && xmlhttp.status==200)
              {
              $("#resultinfo").val(xmlhttp.responseText);
              }
            }
        }
}

function addtr() {
    var trinfo = "<tr><td><input placeholder='参数名称' style='width: 95%;margin: 3px'></td>" +
        "<td><input placeholder='参数值' style='width: 85%;margin: 3px'>" +
        "<button class='btn btn-warning' id='delete-btn' onclick='removetr(event)'>删除参数</button></td></tr>";
    $("#keytable").append(trinfo);
}

// $(function () {
//    $(document).on("click", "#delete-btn", function () {
//         $(this).parents('tr').empty()
//     });
// });

function removetr(ev) {
    $(ev.target).parents("tr").fadeToggle("slow");
}

$(document).ready(function() {
    $("#fortest").click(function () {
        $.get("/forreturn/", function (data) {
            // console.log(data);
            $("#resultinfo").val(JSON.stringify(data))
        });
    });
    $.get("/getinterface/", function (data) {
        // console.log(data);
        // console.log(data["message"]);
        $.each(data["message"],function(index,element){
            $("#interfaceselect").append('<option value=index>'+element+'</option>')
        });
    });
});
