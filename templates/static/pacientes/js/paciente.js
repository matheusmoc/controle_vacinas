function add_carro(){
    container = document.getElementById("form-carro")
    html = 
    "<br>\
    <div class='row'> \
        <div class='col-md'> \
            <input type='text' placeholder='Vacina' class='form-control' name='vacina'>\
        </div>\
        <div class='col-md'>\
            <input type='text' placeholder='Fabricante' class='form-control' name='fabricante'>\
        </div>\
        <div class='col-md'>\
            <input type='number' placeholder='Cód.' class='form-control' name='codigo'>\
        </div>\
    </div>"
    container.innerHTML += html
}

function exibir_form(tipo){
    add_paciente = document.querySelector('#add_paciente')
    att_paciente = document.querySelector('#att_paciente')

    if(tipo == '1'){
        att_paciente.style.display = "none"
        add_paciente.style.display = "block"
    }else if(tipo == "2"){
        att_paciente.style.display = "block"
        add_paciente.style.display = "none"
    }
}

function dados_paciente(){
    paciente = document.querySelector('#paciente_select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    // console.log(csrf_token)

    id_paciente = paciente.value
    
    data = new FormData()
    data.append('id_paciente', id_paciente)
    fetch("/pacientes/atualiza_paciente/",{
        method: "POST",
        headers:{
            'X-CSRFToken': csrf_token,
        },
        body: data
        
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        // console.log(data)
        
        aux = document.querySelector('#form-att-paciente')
        aux.style.display = "block"
        
        id = document.querySelector('#id').value = data['pegar_id_pacientes']['pk']
        // console.log(data['pegar_id_pacientes']['pk'])
        nome = document.querySelector('#nome').value = data['paciente']['nome']
        sobrenome = document.querySelector('#sobrenome').value = data['paciente']['sobrenome']
        cpf = document.querySelector('#cpf').value = data['paciente']['cpf']
        email = document.querySelector('#email').value = data['paciente']['email']

        div_vacinas = document.querySelector('#vacinas')
        div_vacinas.innerHTML = ""  //evita incremento
        
        for(i=0; i<data['vacinas'].length; i++){
            // console.log(data['vacinas'][i]['fields']['vacina'])
            div_vacinas.innerHTML += "\<form action ='/pacientes/update_vacina/"+data['vacinas'][i]['id']+"' method='POST'>\
            <div class='row'>\
                <div class='col-md'>\
                    <input type='text' name='vacina' class='form-control' placeholder='Nome da Vacina' value='"+ data['vacinas'][i]['fields']['vacina']+"'>\
                </div>\
                <div class='col-md'>\
                    <input type='text' name='fabricante' class='form-control' placeholder='Fabricante' value='"+ data['vacinas'][i]['fields']['fabricante']+"'>\
                </div>\
                <div class='col-md'>\
                    <input type='number' name='codigo' class='form-control' placeholder='Código' value='"+ data['vacinas'][i]['fields']['codigo']+"'>\
                </div>\
                <div class='col-md'>\
                    <button class='btn btn-primary' type='submit'>Salvar</button>\
                </div>\
                </form>\
                <a class='btn btn-danger' href='/pacientes/excluir_vacina/"+data['vacinas'][i]['id']+"'>Excluir</a>\
            </div><br>\
            "
        }
    })
}

function update_paciente(){
    id = document.querySelector('#id').value
    nome = document.querySelector('#nome').value
    sobrenome = document.querySelector('#sobrenome').value
    email = document.querySelector('#email').value
    cpf = document.querySelector('#cpf').value

    fetch('/pacientes/update_paciente/'+ id, {
        method: "POST",
        headers:{
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf : cpf
        })
    }).then(function(result){
        return result.json()
    }).then(function(data){
        if( data['status'] == 200 )  {
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']
            console.log('Dados alterados com sucesso!')
        }else{
            console.log('Erro interno ao submeter dados do formulário')
        }
    })
}