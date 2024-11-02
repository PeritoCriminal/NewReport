# newreportapp.tests.test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

class EditUserProfileViewTest(TestCase):
    
    def setUp(self):
        # Cria e autentica um usuário de teste
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@policiacientifica.sp.gov.br'
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_authenticated_user_cannot_access_register(self):
        # Tenta acessar a URL de registro enquanto autenticado
        response = self.client.get(reverse('register'))
        self.assertNotEqual(response.status_code, 200)  # Verifica se a resposta não é 200
        self.assertRedirects(response, reverse('home'))  # Redirecionamento para 'home'
        
    def test_unauthenticated_user_redirected_to_home(self):
        # Acessa a página sem estar autenticado
        self.client.logout()
        response = self.client.get(reverse('edit_user_profile'))
        self.assertRedirects(response, reverse('home'))  # Verifica redirecionamento

    def test_unauthenticated_user_redirected_to_home(self):
        self.client.logout()
        response = self.client.get(reverse('edit_user_profile'))
        self.assertRedirects(response, reverse('home'))

    """
    Esse teste não será mais executado vsito que a troca de senha foi removida do form de edição do usuário.
    def test_password_change_fails_without_current_password(self):
        response = self.client.post(reverse('edit_user_profile'), {
            'username': 'newusername',
            'display_name': 'New Display Name',
            'new_password1': 'newtestpassword456',
            'new_password2': 'newtestpassword456',
        })

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpassword123'))

        # Exibir todas as mensagens para inspecionar o conteúdo
        messages = list(get_messages(response.wsgi_request))
        for message in messages:
            print(f"Mensagem exibida: {message}")  # Linha de depuração para inspecionar as mensagens

        # Verificar por uma mensagem de erro mais genérica, por exemplo, "senha" para cobrir diferentes versões da mensagem
        self.assertTrue(any('senha' in str(message).lower() for message in messages))

        # Status 200, permanecendo na página devido ao erro
        self.assertEqual(response.status_code, 200)
        """