var socket = new SockJS('/websocket-server');
var stompClient = Stomp.over(socket);
stompClient.connect({}, function (frame) {
    stompClient.subscribe('/topic/message', function (txt) {
        var objs = eval(txt.body);
        for(var j = 0;j<objs.length;j++){
            var userId =  objs[j].userId;
            if (userId == 1111){
                $(".list-group").append("<li class=\"list-group-item\">"+objs[j].date+objs[j].content+"</li>");
            }else {
                $(".layui-timeline").append("<li class=\"layui-timeline-item\">\n" +
                    "        <i class=\"layui-icon layui-timeline-axis\">&#xe63f;</i>\n" +
                    "        <div class=\"layui-timeline-content layui-text\">\n" +
                    "            <h3 class=\"layui-timeline-title\">"+objs[j].date+"</h3>\n" +
                    "            <p>"+objs[j].content+"</p>\n" +
                    "        </div>\n" +
                    "    </li>");
            }
        }
    });
    stompClient.subscribe('/topic/add', function (txt) {
        var objs = txt.body;
        if (objs == 0){
            alert("失败");
        }else{
            alert("成功");
        }
    });
    stompClient.subscribe('/topic/sign', function (txt) {
        var objs = txt.body;
        if (objs == 0){
            window.location.href="index.html?count="+111111;
        }else{
            alert("登录失败");
        }
    });
});

function send(txt) {
    $(".list-group").find("li").remove();
    $(".layui-timeline").find("li").remove();
    stompClient.send("/server/send", {}, txt);
}
function addNote() {
    var contents = $(".form-control").val();
    if (contents==null || contents ==""){
        alert("请输入内容");
    }
    stompClient.send("/server/addNote", {}, contents);
}

function sign() {
    var email = $("#email").val();
    var password = $("#password").val();
    if (email == "" || password == "") {
        alert("用户名或密码不能为空！");
    }
    var row2 = {count:email,pwd:password};
    var jsonStr = JSON.stringify(row2);

    stompClient.send("/server/sign", {}, jsonStr);
}

