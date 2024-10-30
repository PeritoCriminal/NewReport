#newreport.tests.test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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

        # Verifica se a resposta é um redirecionamento
        self.assertNotEqual(response.status_code, 200)
        
        # Verifica se redireciona para a página 'home'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))  # Redirecionamento para 'home'
        

    def test_unauthenticated_user_redirected_to_home(self):
        # Acessa a página sem estar autenticado
        response = self.client.get(reverse('edit_user_profile'))
        self.assertRedirects(response, reverse('home'))  # Verifica redirecionamento
