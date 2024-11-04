# newreportapp.tests.test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib import messages
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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

    def test_register_user_with_existing_email(self):
        # Tenta registrar um usuário com um e-mail já cadastrado
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'testuser@policiacientifica.sp.gov.br',  # E-mail existente
        })
        self.assertFormError(response, 'form', 'email', 'Um usuário com esse e-mail já existe.')  # Verifica erro no formulário

    def test_register_user_with_existing_username(self):
        # Tenta registrar um usuário com um nome de usuário já cadastrado
        response = self.client.post(reverse('register'), {
            'username': 'testuser',  # Nome de usuário existente
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@policiacientifica.sp.gov.br',
        })
        self.assertFormError(response, 'form', 'username', 'Um usuário com esse nome já existe.')  # Verifica erro no formulário

    def test_email_confirmation_link_sent(self):
        # Tenta registrar um novo usuário e verifica se o link de confirmação foi enviado
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@policiacientifica.sp.gov.br',
        })
        self.assertEqual(len(mail.outbox), 1)  # Verifica que um e-mail foi enviado
        self.assertIn('Verifique seu e-mail para concluir o cadastro', mail.outbox[0].subject)  # Verifica o assunto do e-mail

    def test_user_is_not_activated_without_confirmation(self):
        # Tenta fazer login sem confirmar o e-mail
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@policiacientifica.sp.gov.br',
        })
        self.assertRedirects(response, reverse('home'))  # Verifica redirecionamento após registro
        user = get_user_model().objects.get(username='newuser')
        self.assertFalse(user.is_active)  # Verifica se o usuário não está ativado

    def test_user_can_be_activated_with_confirmation_link(self):
        # Registra um novo usuário
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@policiacientifica.sp.gov.br',
        })
        user = get_user_model().objects.get(username='newuser')
        
        # Simula o clique no link de confirmação
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        confirmation_response = self.client.get(verification_link)
        
        # Verifica se o usuário foi ativado
        user.refresh_from_db()
        self.assertTrue(user.is_active)  # Verifica se o usuário agora está ativado
        self.assertRedirects(confirmation_response, reverse('login'))  # Verifica redirecionamento após ativação
