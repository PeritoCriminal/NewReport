from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from newreportapp.models.custom_user_model import CustomUserModel
import os
import tempfile
from django.conf import settings
from PIL import Image

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
        
        # Cria uma imagem PNG temporária para o usuário
        self.initial_image_path = tempfile.mktemp(suffix=".png")
        img = Image.new('RGB', (100, 100), color='red')
        img.save(self.initial_image_path)

        with open(self.initial_image_path, 'rb') as img_file:
            self.user.photo = SimpleUploadedFile("initial_photo.png", img_file.read(), content_type="image/png")
            self.user.save()

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

    def test_image_replacement_deletes_old_image(self):
        """Verifica se a imagem antiga é excluída quando o usuário envia uma nova imagem."""
        
        # Cria uma imagem inicial para o usuário
        initial_image_path = tempfile.mktemp(suffix=".png")
        initial_img = Image.new('RGB', (100, 100), color='red')
        initial_img.save(initial_image_path)

        with open(initial_image_path, 'rb') as img_file:
            self.user.photo = SimpleUploadedFile("initial_photo.png", img_file.read(), content_type="image/png")
            self.user.save()

        # Define uma nova imagem para o usuário e salva
        new_image_path = tempfile.mktemp(suffix=".png")
        new_img = Image.new('RGB', (100, 100), color='blue')
        new_img.save(new_image_path)

        with open(new_image_path, 'rb') as new_img_file:
            self.user.photo = SimpleUploadedFile("new_photo.png", new_img_file.read(), content_type="image/png")
            self.user.save()

        # Verifica se a imagem antiga foi deletada
        old_image_path = os.path.join(settings.MEDIA_ROOT, 'user_photos', 'initial_photo.png')
        print(f"Old image path: {old_image_path}")  # Adicione este print para depuração
        self.assertFalse(os.path.exists(old_image_path), "The old image was not deleted.")

        # Limpa as imagens temporárias após o teste
        if os.path.exists(initial_image_path):
            os.remove(initial_image_path)
        if os.path.exists(new_image_path):
            os.remove(new_image_path)


    def tearDown(self):
        """Limpa as imagens após os testes."""
        if self.user.photo:
            if os.path.exists(self.user.photo.path):
                os.remove(self.user.photo.path)
        if os.path.exists(self.initial_image_path):
            os.remove(self.initial_image_path)
