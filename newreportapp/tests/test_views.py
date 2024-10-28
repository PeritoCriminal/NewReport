#newreport.tests.test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

class EditUserProfileViewTest(TestCase):

    def setUp(self):
        # Criação de um usuário de teste e login para simular o acesso autenticado
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
        self.url = reverse('edit_user_profile')
        self.home_url = reverse('home')  # URL da página inicial
        self.login_url = reverse('login')  # URL da página de login

        #Porfavor, reveja somente o método abaixo por enquanto. Depois tratamos os demais.

    def test_access_without_login_redirects_to_login(self):
        """Usuário não logado deve ser redirecionado para a página de login ao tentar acessar a página de edição de perfil."""
        self.client.logout()  # Simula um usuário não autenticado
        response = self.client.get(self.url)
        print(f'\n\n---------------\n{response}\n\n---------------------')
        self.assertRedirects(response, f'{self.login_url}?next=/account/edit_user_profile/')
        # self.assertRedirects(response, f'{self.login_url}?next={self.url}')  # Ajuste para refletir o prefixo correto

    def test_access_without_login_allows_home_access(self):
        """Usuário não logado deve poder acessar a página inicial."""
        self.client.logout()  # Simula um usuário não autenticado
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)  # Verifica se a resposta é 200 OK

    def test_access_without_login_allows_login_access(self):
        """Usuário não logado deve poder acessar a página de login."""
        self.client.logout()  # Simula um usuário não autenticado
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)  # Verifica se a resposta é 200 OK

    def test_view_renders_correct_template_for_authenticated_user(self):
        """Verifica se a view renderiza o template correto para usuários logados."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/edit_user_profile.html')

    def test_profile_update_success(self):
        """Verifica se a atualização do perfil é realizada com dados válidos."""
        response = self.client.post(self.url, {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
        })

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Perfil atualizado com sucesso!')
        self.assertRedirects(response, reverse('home'))

    def test_profile_update_with_invalid_data(self):
        """Verifica o comportamento com dados inválidos."""
        response = self.client.post(self.url, {
            'username': '',  # Nome de usuário inválido (vazio)
            'email': 'invalid-email'  # Email em formato inválido
        })

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, '')  # O nome de usuário não deve ter sido alterado
        self.assertNotEqual(self.user.email, 'invalid-email')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Erro ao atualizar o perfil. Verifique os dados e tente novamente.')
        self.assertEqual(response.status_code, 200)  # Deve recarregar a página com erros
