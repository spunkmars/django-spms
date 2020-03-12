function run_shell(s_id, url) {
    var getdata;
    var type = document.getElementById('type').value;
    var val = document.getElementById('val').value;
    var command = document.getElementById('command').value;
    var idc = document.getElementById('idc').value;
    var run_type = document.getElementById('run_type').value;
    var send_data = {'type':type, 'val':val, 'command':command, 'idc':idc, 'run_type':run_type};
    getdata = {
        poll: function(){
            $.ajax({url: url,
                    //type: "GET",
                    type: "POST",
                    data: send_data,
                    dataType: 'json',
                    success: getdata.onSuccess,
                    error: getdata.onError});
        },
        onSuccess: function(data, dataStatus){
          //alert("A :  " + data.a)
           //$("#shell_result").append(data.val);
           //$("#shell_result").append('<br />');
           s_data = data.val
           s_data = s_data.replace(/\&#39\;/g, "'");
           s_data = s_data.replace(/\&amp\;/g, "&");
           document.getElementById('shell_result').value = s_data
           var fields = data.fields
        },
        onError: function(){
           alert('发生错误!');
           return false;
        }
    };
    getdata.poll();
}


function clear_shell_result(s_id) {
    document.getElementById('shell_result').value = '';
}


function clear_command(s_id) {
    document.getElementById('command').value = '';
}