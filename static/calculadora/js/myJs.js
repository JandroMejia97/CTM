function filterTable(idInput, idTable){
    filter = document.getElementById(idInput).value.toUpperCase();
    $("#"+idTable+" tr").filter(function(){
        $(this).toggle($(this).text().toUpperCase().indexOf(filter)>-1)
    });
};
function filterSelect(idInput, idSelect){
    filter = document.getElementById(idInput).value.toUpperCase();
    $("#"+idSelect+" li").filter(function(){
        $(this).toggle($(this).text().toUpperCase().indexOf(filter)>-1)
    });
}
function deploySelect(select){
    var event = new MouseEvent('mousedown');
    select.dispatchEvent(event);
}
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
    if(message.alert=='exclamation'){
        $(".messages").append(
            "<div class='alert alert-danger alert-dismissable'>"
                +"<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>"
                +"<i class='fa fa-"+message.alert+"'></i> "
                +message.result
            +"</div>"
        );
    }else{
        $(".messages").append(
            "<div class='alert alert-success alert-dismissable'>"
                +"<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>"
                +"<i class='fa fa-"+message.alert+"'></i> "
                +message.result
            +"</div>"
        );
    }
    
}

function getLocalidades(id, seleccion){
    console.log('GET: CIUDADES');
    console.log('AJAX: LOCALIDADES');
    var id = $('#'+id).val();

    $.ajax({
        url: '/ajax/localidades/',
        type: 'GET',
        data: {
            'id': id,
        },
        success: function(){
            console.log("SUCCESS");
        },
        dataType: 'json'
    }).done(function(data){
    $("#"+seleccion).empty();
        if(data.response != null){
            $.each(data.response, function(index, value){
                $("#"+seleccion).append(
                    "<option id='"+value.pk + "' value='" +
                    value.pk + "'>" + value.nombre + "</option>");
            });
            $("#"+seleccion).removeAttr('disabled');
        }else{
            $("#"+seleccion).empty();
            $("#"+seleccion).append('<option value="" selected="">---------</option>');
            $("#"+seleccion).attr('disabled','disabled');
        }
    }).fail(function() {
        console.log("error");
    }).always(function(data) {
        addMessage(data.message);
        console.log(data.message);
        console.log("complete");
    });
  }
function enabledInputs(formId, buttonsId){
    $("#"+formId+" input").prop('disabled', !$("#"+formId+" input").prop('disabled'));
    $("#"+buttonsId).prop('hidden', !$("#"+buttonsId).prop('hidden'));
}
function reloadIframe(inputId){
    console.log("RELOAD IFRAME");
    var input = document.getElementById(inputId).value;
    console.log(input)
    $("#iframe").empty();
    $("#iframe").append(input);
}

function addProducto(cantidad){
    $.ajax({
        type: "GET",
        url: '/ajax/formset/producto/',
        data: {
            'cantidad': cantidad+1,
        },
        success: function(data){
            console.log("SUCCES");
            $("#productosAdd").empty();
            $("#productosAdd").append(data);
        },
        fail: function(){
            console.log("FAIL");
        }
    })
}
function deleteProducto(cantidad){
    $.ajax({
        type: "GET",
        url: '/ajax/formset/producto/',
        data: {
            'cantidad': cantidad-1,
        },
        success: function(data){
            console.log("SUCCES");
            $("#productosAdd").empty();
            $("#productosAdd").append(data);
        },
        fail: function(){
            console.log("FAIL");
        }
    })
}

function addFieldSet(contenderClass, blockClass){
    var numero = $("."+contenderClass+" ."+blockClass).length; 
    var newClone = $("."+contenderClass).clone("."+blockClass);
    newClone.prop('id', 'Add'+numero+1);
    newClone.prop('onclick', "addFieldSet(contenderClass, blockClass, numero)");
    $("."+contenderClass).append(clone);
}
$('.add-more-btn').click(function() {
    var clone = $('.form-main').clone('.form-block');
    $('.form-main').append(clone);
  });