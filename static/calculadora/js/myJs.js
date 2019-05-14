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
                        //+"<a href=\"#\" onclick=\"getRegion(\'id_pais\', \'id_ciudad\', "+value.id+", \'"+value.nombre.toUpperCase()+"\', \'"+anteriorFiltro+"\', \'"+nuevoFiltro+"\')\">"
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

  function getPaises(id, seleccion){
    console.log('GET: PAISES');
    console.log('AJAX: CIUDADES');
    $.ajax({
        url: '/ajax/paises/',
        type: 'GET',
        data: {
            'id': id,
        },
        success: function(data){
            console.log("SUCCESS");
        },
        dataType: 'json'
    }).done(function(data){
    $("#paises").empty();
        if(data.response != null){
            $.each(data.response, function(index, value){
                $("#paises").append(
                    "<li>"
                        +"<a href=\"#\" onclick=\"getCiudades("+value.id+", \'"+value.nombre.toUpperCase()+"\')\">"
                          + value.nombre.toUpperCase()
                        +"</a>"
                    +"</li>");
            });
            $("#pais_filtro").removeAttr('disabled');
            $("#continente_filtro").val(seleccion);
        }else{
            $("#paises").empty();
            $("#paises").append('<li><a href="#">Sin resultados</a></li>');
            $("#continente_filtro").empty();
            $("#continente_filtro").val(seleccion);
            $("#pais_filtro").attr('disabled','disabled');
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