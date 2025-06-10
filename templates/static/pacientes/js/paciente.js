new Vue({
  el: '#pacientes',
    data: {
        formType: '', // 'create' ou 'update'
        csrfToken: document.querySelector('[name=csrfmiddlewaretoken]').value,
        novoPaciente: {
            nome: '',
            sobrenome: '',
            email: '',
            cpf: '',
            vacinas: []
        },
        pacientes: [],
        pacienteSelecionado: '',
        pacienteSelecionadoId: '',
        paciente: {},
        vacinas: []
    },
    delimiters: ['((', '))'], 
    methods: {
        toggleForm(type) {
            // Se o botão clicado já estiver ativo, desativa (limpa formType)
            if (this.formType === type) {
                this.formType = '';
                this.pacienteSelecionado = ''; 
            } else {
                this.formType = type;
            }
            
            if (type === 'update') {
                this.showUpdateForm();
            } else {
                this.hideUpdateForm();
            }
        },
        showUpdateForm() {
            this.pacienteSelecionado = '';
        },
        hideUpdateForm() {
            this.pacienteSelecionado = '';
        },

        addVacina() {
            this.novoPaciente.vacinas.push({
            vacina: '',
            fabricante: '',
            codigo: ''
            });
        },
        selectCreateForm() {
            this.formType = 'create';
            this.novoPaciente = {
                nome: '',
                sobrenome: '',
                email: '',
                cpf: '',
                vacinas: []
            };
        },
        selectUpdateForm() {
            this.formType = 'update';
            this.pacienteSelecionado = '';
        },
        cadastrarPaciente() {
            const data = new FormData();

            data.append('nome', this.novoPaciente.nome);
            data.append('sobrenome', this.novoPaciente.sobrenome);
            data.append('cpf', this.novoPaciente.cpf);
            data.append('data_nascimento', this.novoPaciente.data_nascimento)
            data.append('vacinas', JSON.stringify(this.novoPaciente.vacinas));

            fetch("/pacientes/api/pacientes/", {
                method: "POST",
                headers: {
                    'X-CSRFToken': this.csrfToken
                },
                body: data
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 200) {
                    alert("Paciente cadastrado com sucesso!");
                    this.selectCreateForm(); 
                } else {
                    alert("Erro: " + data.message);
                }
            })
            .catch(error => {
                console.error("Erro ao cadastrar paciente:", error);
            });
        },

        buscarPacientes() {
            fetch('/pacientes/api/pacientes/', {
                method: "GET",
                headers: {
                    'Accept': 'application/json'
                },
            })  
            .then(response => response.json())
            .then(data => {
                this.pacientes = data.pacientes || data; 
                console.log(data)
            })
            .catch(error => {
                console.error('Erro ao buscar pacientes:', error);
            });
        },

        showInfoPaciente() {
            const paciente = this.pacientes.find(p => p.id === parseInt(this.pacienteSelecionadoId));
            this.pacienteSelecionado = paciente || {};
        },

        atualizarPaciente() {
            fetch(`/pacientes/api/update_paciente/${this.pacienteSelecionado.id}/`, {
                method: "POST",
                headers: {
                    'X-CSRFToken': this.csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.pacienteSelecionado)
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 200) {
                    alert("Atualizado com sucesso!");
                } else {
                    console.log(data)
                    alert("Erro ao atualizar: " + data.message);
                }
            })
            .catch(err => {
                console.error("Erro na atualização:", err);
            });
        }
    },
    mounted() {
        this.buscarPacientes();
    },
});
