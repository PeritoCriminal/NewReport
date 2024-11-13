#newreportapp/models/report/header_report_model.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date

class HeaderReportModel(models.Model):
    """ A classe HeaderReportModel tem atributos e métdodos comuns dos relatórios em geral """

    report_date = models.DateField('Data do Registro', auto_now_add=True) 
    designation_date = models.DateField('Data de Designação', default=timezone.localdate) 
    occurrence_date = models.DateField('Data da Ocorrência', default=timezone.localdate) 
    occurrence_time = models.TimeField('Hora do Atendimento', null=True, default='00:00:00')
    call_date = models.DateField('Data do Acionamento', default=timezone.localdate) 
    call_time = models.TimeField('Hora do Acionamento', null=True, default='00:00:00')
    service_date = models.DateField('Data do Atendimento', default=timezone.localdate) 
    service_time = models.TimeField('Hora do Atendimento', null=True, default='00:00:00')
    report_number = models.CharField('Número do Laudo', max_length=100, default='', null=True)
    city = models.CharField('Cidade', max_length=100, default='Limeira', null=True)
    protocol_number = models.CharField('Número do Protocolo', max_length=200, default='', null=True)
    police_report_number = models.CharField('Número do Boletim de Ocorrência', max_length=200, default='', null=True)
    examination_objective = models.CharField('Objetivo do Exame', max_length=300, default='')
    incident_nature = models.CharField('Natureza da Ocorrência', max_length=300, default='', null=True)
    police_station = models.CharField('Distrito Policial', max_length=200, default='', null=True)
    requesting_authority = models.CharField('Autoridade Requisitante', max_length=200, default='', null=True)
    institute_director = models.CharField('Diretor do Instituto', max_length=200, default='')
    institute_unit = models.CharField('Núcleo do Instituto', max_length=200, default='')
    forensic_team_base = models.CharField('Base da Equipe de Perícias', max_length=200, default='')
    expert_display_name = models.CharField('Perito', max_length=200, default='')
    reporting_expert = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Perito Relator'
    )    
    considerations = models.TextField('Considerações', blank=True, default='')
    conclusion = models.TextField('Conclusão', blank=True, default='')

    def save(self, *args, **kwargs):
        """Sobrescreve o método save para copiar o full_name do usuário"""
        if self.reporting_expert:
            print(f'Nome completo do usuário: {self.expert_display_name}')
            self.expert_display_name = self.expert_display_name
        else:
            print(f'Não tem o usuário.')
        super().save(*args, **kwargs)


    @classmethod
    def notify_default_dates(cls):
        """Retorna uma mensagem para o usuário caso haja datas com valor default"""
        return """
        Algumas datas estão com o valor padrão de 01-01-1900. Reveja as antes de finalizar o relatório.
        """
    
    
    def dateToForm(self, date_field = '1900-01-01'):
        """Converte qualquer uma das datas cadastradas no formato 'yyyy-mm-dd'"""
        if date_field:
            try:
                return date_field.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                return '1900-01-01'
        return '1900-01-01'


    def dateToDoc(self, date_field=date(1900, 1, 1)):
        """Converte qualquer uma das datas cadastradas no formato por extenso"""

        if date_field:
            try:
                # Mapeamento manual dos meses em português
                meses_portugues = {
                    1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
                    5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
                    9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
                }

                # Extrai o dia, o mês e o ano do objeto date
                dia = date_field.day
                mes = meses_portugues[date_field.month]
                ano = date_field.year

                # Retorna o formato desejado
                return f'{dia} de {mes} de {ano}'

            except (ValueError, AttributeError):
                return '1 de janeiro de 1900'

        return '1 de janeiro de 1900'

    
    
    def hourToForm(self, time_field = '00:00'):
        """Converte qualquer uma das horas cadastradas no formato 'HH:MM'"""
        if time_field:
            try:
                return time_field.strftime('%H:%M')
            except (ValueError, AttributeError):
                return '00:00'
        return '00:00'
    

    def hourToDoc(self, time_field='00:00'):
        """Converte qualquer uma das horas cadastradas no formato 'HHhMMmin' ou 'HHh' se os minutos forem 00"""
        if time_field:
            try:
                # Verifica se os minutos são 00
                if time_field.strftime('%M') == '00':
                    return time_field.strftime('%Hh')
                else:
                    return time_field.strftime('%Hh%Mmin')
            except (ValueError, AttributeError):
                return '00h'
        return '00h'
    

    def get_director(self):
        if self.institute_director.startswith('Dra'):
            return f'pela Diretora deste Instituto de Criminalística, a Perita Criminal {self.institute_director}'
        elif self.institute_director.startswith('Dr.'):
            return f'pelo Diretor deste Instituto de Criminalística, o Perito Criminal {self.institute_director}'
        return f'pelo(a) Diretor(a) deste Instituto de Criminalística, o(a) Perito(a) Criminal {self.institute_director}'

    def get_expert(self):
        if self.expert_display_name.startswith('Dra.'):
            return f'designada a perita criminal {self.expert_display_name}'
        elif self.expert_display_name.startswith('Dr.'):
            return f'designado o perito criminal {self.expert_display_name}'
        return f'designado(a) o(a) perito(a) criminal {self.expert_display_name}'

    def get_authority(self):
        if self.requesting_authority.startswith('Dra.'):
            return f'a Delegada de Polícia {self.requesting_authority}'
        elif self.requesting_authority.startswith('Dr.'):
            return f'o Delegado de Polícia {self.requesting_authority}'
        return f'o(a) Delegado(a) de Polícia {self.requesting_authority}'

    def makePreamble(self):
        director = self.get_director()
        expert = self.get_expert()
        authority = self.get_authority()
        designation_date = self.dateToDoc(self.designation_date)

        return (
            f"Em {designation_date}, na cidade de {self.city} "
            f"e no Instituto de Criminalística da Superintendência da Polícia Técnico-Científica, " 
            f"da Secretaria de Segurança Pública do Estado de São Paulo, em conformidade com o disposto no art. "
            f"178 do Decreto-Lei 3689, de 3 de outubro de 1941, e no Decreto-Lei 42847, "
            f"de 9 de fevereiro de 1998, {director}, "
            f"foi {expert} para proceder ao exame pericial especificado em requisição "
            f"assinada pela Autoridade Policial, {authority}."
        )


    def __str__(self):
        return f'Relatório {self.report_number} - Perito: {self.expert_display_name}'

    class Meta:
        verbose_name = 'Relatório Pericial'
        verbose_name_plural = 'Relatórios Periciais'
