function empty(v) {
    switch (typeof v) {
        case 'undefined' :
            return true;
        case 'string' :
            if (v.trim().length == 0) return true;
            break;
        case 'boolean' :
            if (!v) return true;
            break;
        case 'number' :
            if (0 === v) return true;
            break;
        case 'object' :
            if (null === v) return true;
            if (undefined !== v.length && v.length == 0) return true;
            for (var k in v) {
                return false;
            }
            return true;
            break;
    }
    return false;
}


// window.onload = function () {
//     $.ajax({
//         url: "/commonx/language/list/",
//         type: "POST",
//         data: "",
//         dataType: "text",
//         success: function (data) {
//             var obj = jQuery.parseJSON(data);
//             form_code = lang_select(obj);
//             document.getElementById('language').innerHTML = form_code;
//         },
//         error: function (data) {
//             form_code = '';
//             document.getElementById('language').innerHTML = form_code;
//         }
//     });
// }


function lang_select(data) {
    var form_code = '<option value="en">-----------</option>';

    var now_s = data[1];
    for (key in data[0]) {
        if (!empty(data[0][key])) {
            if (key == now_s) {
                form_code = form_code + "<option value='" + key + "' selected> " + data[0][key] + "</option>";
            } else {
                form_code = form_code + "<option value='" + key + "'> " + data[0][key] + "</option>";
            }
        }
    }
    return form_code;
}


function on_change() {
    s_value = $('#language').val();
    $.ajax({
        url: "/commonx/language/select/",
        type: "POST",
        data: {"language": s_value},
        dataType: "text",
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            alert('Error');
        }
    });
}


function setCookie(name, value, expires) {
    document.cookie = name + "=" + escape(value) + ";expires='" + expires + "';path=/";
}


function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");

    if (arr = document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}


function getAutoVal(s_id, url, d_type) {
    var getdata;
    var send_data = {'d_type': d_type};
    getdata = {
        poll: function () {
            $.ajax({
                url: url,
                //type: "GET",
                type: "POST",
                data: send_data,
                dataType: 'json',
                success: getdata.onSuccess,
                error: getdata.onError
            });
        },
        onSuccess: function (data, dataStatus) {
            //alert("A :  " + data.a)
            //console.log("E :  " + data.e)
            document.getElementById(s_id).value = data.val;
            var fields = data.fields
        },
        onError: function () {
            alert('参数传入错误!');
            return false;
        }
    };
    getdata.poll();
}

//获取url path部分
function getUrlRelativePath() {
    var url = document.location.toString();
    var arrUrl = url.split("//");

    var start = arrUrl[1].indexOf("/");
    var relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符

    if (relUrl.indexOf("?") != -1) {
        relUrl = relUrl.split("?")[0];
    }
    return relUrl;
}

//获取url中的参数方法
function getUrlParam(name) {  //构造一个含有目标参数的正则表达式对象
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]);
    return null;

}


//获取url中的参数方法
function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    }
    return (false);
}


function convert_view_name_to_url(view_name, param) {
    var r_url = undefined;
    $.ajax({
        type: "POST",
        data: {'view_name': view_name, 'view_param': JSON.stringify(param)},
        url: '/commonx/convert_view_name_to_url/',
        dataType: 'json',
        async: false, //同步执行
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success: function (data, textStatus) {
            r_url = data.url;
            return false;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            return false;
        }
    });
    return r_url;
}


function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}