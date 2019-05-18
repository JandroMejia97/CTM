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
}

function getCiudades(id, seleccion){
    console.log('GET: PAISES');
    console.log('AJAX: CIUDADES');
    $.ajax({
        url: '/ajax/ciudades/',
        type: 'GET',
        data: {
            'id': id,
        },
        success: function(data){
            console.log("SUCCESS");
        },
        dataType: 'json'
    }).done(function(data){
    $("#ciudades").empty();
        if(data.response != null){
            $.each(data.response, function(index, value){
                $("#ciudades").append(
                    "<li>"
                        +"<a href=\"#\">"
                          + value.nombre.toUpperCase()
                        +"</a>"
                    +"</li>");
            });
            $("#ciudad_filtro").removeAttr('disabled');
            $("#pais_filtro").val(seleccion);
        }else{
            $("#ciudades").empty();
            $("#ciudades").append('<li><a href="#">Sin resultados</a></li>');
            $("#pais_filtro").empty();
            $("#pais_filtro").val(seleccion);
            $("#ciudad_filtro").attr('disabled','disabled');
        }
    }).fail(function(data) {
        console.log("error");
    }).always(function(data) {
        addMessage(data.message);
        console.log(data.message);
        console.log("complete");
    });
  }

  function getLocalidades(id, seleccion){
    console.log('GET: CIUDADES');
    console.log('AJAX: LOCALIDADES');
    $.ajax({
        url: '/ajax/localidades/',
        type: 'GET',
        data: {
            'id': id,
        },
        success: function(data){
            console.log("SUCCESS");
        },
        dataType: 'json'
    }).done(function(data){
    $("#localidades").empty();
        if(data.response != null){
            $.each(data.response, function(index, value){
                $("#localidades").append(
                    "<li>"
                        +"<a href=\"#\">"
                          + value.nombre.toUpperCase()
                        +"</a>"
                    +"</li>");
            });
            $("#localidad_filtro").removeAttr('disabled');
            $("#ciudad_filtro").val(seleccion);
        }else{
            $("#localidades").empty();
            $("#localidades").append('<li><a href="#">Sin resultados</a></li>');
            $("#ciudad_filtro").empty();
            $("#ciudad_filtro").val(seleccion);
            $("#localidad_filtro").attr('disabled','disabled');
        }
    }).fail(function(data) {
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