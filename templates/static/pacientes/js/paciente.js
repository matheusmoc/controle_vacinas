function add_carro(){

    container = document.getElementById("form-carro")

    html = "<br><div class='row'> <div class='col-md'> <input type='text' placeholder='Vacina' class='form-control' name='vacina'></div> <div class='col-md'> <input type='text' placeholder='Fabricante' class='form-control' name='fabricante'> </div> <div class='col-md'><input type='number' placeholder='Cód.' class='form-control' name='codigo'> </div></div>"

    container.innerHTML += html


}