/**
 * Created by YangQ on 2017/7/7.
 */

function getrut() {
    var a = document.getElementById("num1").value;
    var b = document.getElementById("fh").value;
    var c = document.getElementById("num2").value;
    if (b=='+'){
        var d=a+c
    }
    else if (b=='-'){
        var d=a-c
    }
    else {
        var d=a*c
    }
    document.getElementById("result").value=d;

}

function write(){
    document.write('123')
}

