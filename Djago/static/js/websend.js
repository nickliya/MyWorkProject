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
        "<button class='btn btn-warning' id='delete-btn' onclick='removetr(event)'>" +
        "<span class='glyphicon glyphicon-minus' aria-hidden='true'></span> 删除参数</button></td></tr>";
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
    // 发送请求
    $("#fortest").click(function () {
        $.get("/returndata/", function (data) {
            // console.log(data);
            $("#resultinfo").val(JSON.stringify(data))
        });
    });

    // 读取数据库保存的接口
    $.get("/getinterface/", function (data) {
        // console.log(data);
        // console.log(data["message"]);
        $.each(data["message"],function(index,element){
            $("#interfaceselect").append('<option value='+index+'>'+element+'</option>')
        });
    });

    // 选择监听，并列出相应接口的参数
    $("#interfaceselect").select(function(){
        var interfacename=$("#interfaceselect").find("option:selected").text();
        // console.log(interfacename);
        var postinfo={
            "interfacename":interfacename
        };
        $.post("/getinterfacepayload/", postinfo, function (data) {
            console.log(data["message"]);
            $.each(data["message"]["payload"],function(index,element){
                // console.log(index,element);

                var trinfo = "<tr><td><input placeholder='参数名称' style='width: 95%;margin: 3px' value="+index+"></td>" +
                        "<td><input placeholder='参数值' style='width: 85%;margin: 3px' value="+element+">" +
                        "<button class='btn btn-warning' id='delete-btn' onclick='removetr(event)'>" +
                        "<span class='glyphicon glyphicon-minus' aria-hidden='true'></span> 删除参数</button></td></tr>";
                $("#keytable").append(trinfo);
            });
        });
    });

    if ("WebSocket" in window){
        console.log("yes");
        var ws = new WebSocket('ws://192.168.6.235:8000/socket/');
        ws.onopen = function(){
            console.log("123");
            ws.send("(1*7c|a3|106,201|101,865328028513165|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)")
        };
        ws.onmessage = function(evt){
            var info = evt.data;
            console.log(info)
        };
        ws.onclose =function(){
        }
    }
    else {
        console.log("no")
    }
});