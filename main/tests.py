from django.test import TestCase, Client
from django.contrib.auth.models import User
from main.models import Profile
class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/skibidi/')
        self.assertEqual(response.status_code, 404)

class DashboardModuleTest(TestCase):
    def setUp(self):
        # buat user
        self.user = User.objects.create_user(username='user.login1', email='user@test.com', password='userPW1')
        Profile.objects.create(user=self.user, phone_number="08123456789", gender="M")

        # buat admin
        self.admin = User.objects.create_user(username='admin.login1', email='admin@test.com', password='adminPW1', is_staff=True)
        Profile.objects.create(user=self.admin, phone_number="08987654321", gender="M")

        self.client = Client()
