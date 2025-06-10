from django.urls import path
from .views import PacienteView, VacinaView, RelatorioStatusVacinalView, HistoricoVacinalView, PacienteViewAPI

urlpatterns = [
    path('', PacienteView.as_view(), name="pacientes"),
    path('api/pacientes/', PacienteViewAPI.as_view(), name="api_pacientes"),
    path('api/atualiza_paciente/', PacienteViewAPI.att_paciente, name="atualiza_paciente"),
    path('api/update_paciente/<int:id>/', PacienteViewAPI.update_paciente, name="update_paciente"),
    
    path('excluir_vacina/<int:id>/', VacinaView.as_view(), name="excluir_vacina"),
    path('update_vacina/<int:id>/', VacinaView.update_vacina, name="update_vacina"),
    
    path('report_vaccination/', RelatorioStatusVacinalView.get_report, name='relatorio_vacinal'),
    path('history_vaccination/', HistoricoVacinalView.get_history, name='historico_vacinal'),

]
