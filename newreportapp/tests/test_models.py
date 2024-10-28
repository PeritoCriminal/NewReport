from django.test import TestCase
from newreportapp.models.custom_user_model import CustomUserModel

class CustomUserModelTest(TestCase):
    
    def setUp(self):
        # Cria um usuário de teste com valores específicos
        self.user = CustomUserModel.objects.create_user(
            username='testuser',
            password='testpass123',
            access_level=CustomUserModel.EDITOR,
            display_name='Test User',
            gender='M',
        )
    
    def test_user_creation(self):
        """Verifica se o usuário foi criado corretamente."""
        user = CustomUserModel.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_default_access_level(self):
        """Verifica se o nível de acesso padrão é 'VIEWER'."""
        user = CustomUserModel.objects.create_user(username='defaultuser', password='defaultpass123')
        self.assertEqual(user.access_level, CustomUserModel.VIEWER)
    
    def test_str_method(self):
        """Verifica se o método __str__ retorna o username corretamente."""
        self.assertEqual(str(self.user), 'testuser')
    
    def test_display_name_field(self):
        """Verifica se o campo display_name é armazenado corretamente."""
        self.assertEqual(self.user.display_name, 'Test User')
    
    def test_gender_field(self):
        """Verifica se o campo gender aceita e armazena corretamente os valores."""
        self.assertEqual(self.user.gender, 'M')
    
    def test_permissions(self):
        """Verifica as permissões definidas no Meta."""
        user = CustomUserModel.objects.get(username='testuser')
        self.assertIn(('can_view_content', 'Can view content'), user._meta.permissions)
        self.assertIn(('can_edit_content', 'Can edit content'), user._meta.permissions)
        self.assertIn(('can_administrate', 'Can administrate'), user._meta.permissions)
