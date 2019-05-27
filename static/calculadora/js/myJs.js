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
};

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
    
};

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
            $("#"+seleccion).append('<option value="" selected="">---------</option>');
            $.each(data.response, function(index, value){
                $("#"+seleccion).append(
                    "<option id='"+value.id + "' value='" +
                    value.id + "'>" + value.nombre + "</option>");
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

function updateElementIndex(elemento, prefijoForm, indice){
    var id_regex = new RegExp('(' + prefijoForm + '-\\d+)');
    var reemplazo = prefijoForm + '-' + indice;
    if($(elemento).attr("for")){
        $(elemento).attr("for", $(elemento).attr("for").replace(id_regex, reemplazo));
    }
    if($(elemento).attr("id")){
        $(elemento).attr("id", $(elemento).attr("id").replace(id_regex, reemplazo));
    }
    if(elemento.id){
        elemento.id = elemento.id.replace(id_regex, reemplazo);
    }
    if(elemento.name){
        elemento.name = elemento.name.replace(id_regex, reemplazo);
    }
    if($(elemento).attr('onclick')){
        $(elemento).attr("onclick", $(elemento).attr("onclick").replace(id_regex, reemplazo));
    }
}

function cloneMore(prefijoFila, classFormSet){
    var idFilaOriginal = '#'+prefijoFila+'-row';
    var nuevaFila = $(idFilaOriginal).clone(true);
    var total = parseInt($('#id_'+classFormSet+'-TOTAL_FORMS').val()); // Obteniendo la cantidad actual de formularios
    nuevaFila.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function(){
        var nombre = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + nombre;
        $(this).attr({'name': nombre, 'id': id}).val('').removeAttr('checked');
    });
    nuevaFila.find('label').each(function(){
        var valor = $(this).attr('for');
        if(valor){
            valor = valor.replace('-' + (total-1) + '-', '-' + total + '-');
            $(this).attr({'for': valor});
        }
    });
    var anteriorFila = $(idFilaOriginal);
    idFilaNueva = prefijoFila.replace('-' + (total-1), '-' + total)+'-row';
    prefijoFilaNueva = prefijoFila.replace('-' + (total-1) , '-' + total);
    nuevaFila.find('span').each(function(){
        var id = $(this).attr('id');
        if(id){
            id = id.replace('-' + (total-1) + '-', '-' + total + '-');
            $(this).attr({
                'id': id,
                'onclick': "cloneMore('"+prefijoFilaNueva+"', '"+classFormSet+"')"
            });
        }
    })
    nuevaFila.prop('id', idFilaNueva);
    anteriorFila.find('#add-' + prefijoFila + '-btn').each(function(){
        var id = $(this).attr('id');
        if(id){
            id = id.replace('add', 'remove');
            $(this).attr({
                'id': id,
                'onclick': 'deleteForm("'+prefijoFila+'", "'+classFormSet+'")'
            });
        }
    })
    .empty().append('<i class="fa fa-trash-alt fw"></i>')
    .removeClass('btn-primary').addClass('btn-danger');
    total++;
    $('#id_'+classFormSet+'-TOTAL_FORMS').val(total);
    $(idFilaOriginal).after(nuevaFila);
    return false;
}

function deleteForm(prefijoFila, classFormSet){
    var idFilaOriginal = '#'+prefijoFila+'-row';
    var totalAnterior = parseInt($('#id_' + classFormSet + '-TOTAL_FORMS').val());
    if(totalAnterior > 1){
        var btn = document.getElementById('remove-'+prefijoFila+'-btn')
        btn.closest(idFilaOriginal).remove();
        var forms = $('.'+classFormSet);
        $('#id_' + classFormSet + '-TOTAL_FORMS').val(totalAnterior-1);
        var totalActual = parseInt($('#id_' + classFormSet + '-TOTAL_FORMS').val());
        for(var i=0, formCount=forms.length; i<formCount;i++){
            $(forms.get(i)).find(':input').each(function(){
                updateElementIndex(this, classFormSet, i);
            });
            $(forms.get(i)).find('label').each(function(){
                updateElementIndex(this, classFormSet, i);
            });
            $(forms.get(i)).find('span').each(function(){
                updateElementIndex(this, classFormSet, i, (i+1));
            });
            updateElementIndex($(forms.get(i)), classFormSet, i);
        }
    }
}