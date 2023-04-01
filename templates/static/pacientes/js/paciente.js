function add_carro(){
    container = document.getElementById("form-carro")
    html = "<br><div class='row'> <div class='col-md'> <input type='text' placeholder='Vacina' class='form-control' name='vacina'></div> <div class='col-md'> <input type='text' placeholder='Fabricante' class='form-control' name='fabricante'> </div> <div class='col-md'><input type='number' placeholder='Cód.' class='form-control' name='codigo'> </div></div>"
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
        document.querySelector('#form-att-paciente').style.display = "block"
        nome = document.querySelector('#nome')
        nome.value = data['nome']

        sobrenome = document.querySelector('#sobrenome')
        sobrenome.value = data['sobrenome']

        cpf = document.querySelector('#cpf')
        cpf.value = data['cpf']

        email = document.querySelector('#email')
        email.value = data['email']
    })
}