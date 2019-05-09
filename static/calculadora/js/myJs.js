function addMessage(message){
    if(message.user.first_name && message.user.last_name){
        var user=message.user.first_name+' '+message.user.last_name;
    }
    else{
        if (message.user.first_name){
            var user = message.user.first_name;
        }
        else{
            var user = message.user.username;
        }
    }
    $("#messages").append(
        "<li class='message-preview'>"
            +"<a href=''>"
                +"<div class='media'>"
                    +"<div class='media-body'>"
                        +"<h5 class='media-heading'>"
                            +user
                        +"</h5>"
                        +"<p class='small text-muted'>"
                            +"<i class='fa fa-clock-o'></i>"
                            +message.hora
                        +"</p>"
                        +"<p><i class='fa fa-"+message.alert+"-circle'></i> "
                            +message.result
                        +"</p>"
                    +"</div>"
                +"</div>"
            +"</a>"
        +"</li>"
    );
}

function getData(sendData, depData){
    console.log('GET: ', sendData);
    var send = $("#"+sendData).val();
    console.log('AJAX: '+sendData);
    $.ajax({
        url: '/ajax/'+depData+'/',
        type: 'GET',
        data: {
            'data': send,
            'case': sendData,
        },
        success: function(data){
            console.log("SUCCESS");
        },
        dataType: 'json'
    }).done(function(data){
    $("#"+depData).empty();
        if(data.response != null){
            $("#"+depData).append('<option value="" selected="">---------</option>');
            $.each(data.response, function(index, value){
                $("#"+depData).append(
                    "<option id='"+value.id + "' value='" + value.id + "'>"
                        + value.nombre 
                    + "</option>");
            });
            $("#"+depData).removeAttr('disabled');
        }else{
            $("#"+depData).append('<option value="" selected="">---------</option>');
            $("#"+depData).attr('disabled','disabled');
        }
    }).fail(function(data) {
        console.log("error");
    }).always(function(data) {
        addMessage(data.message);
        console.log(data.message);
        console.log("complete");
    });
  }
