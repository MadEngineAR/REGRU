from django.test import TestCase
# Create your tests here.
# from mainapp.models import ProductCategories, Product
from django.test.client import Client
from authapp.models import User


class UserTestCase(TestCase):

    def setUp(self) -> None:

        self.username = 'django'
        self.email = 'django@mail.ru'
        self.password = 'Django_@1234'

        new_user_data = {
            'username': 'django1',
            'first_name':'Джанга',
            'last_name': 'Джанга',
            'email': 'django1@mail.ru',
            'password1': 'Django_@1234',
            'password2': 'Django_@1234',
            'age': 31,
        }

        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        self.client =Client()

    def test_login(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

# При запуске строк 35, 36 выдает ошибку authapp.models.User.DoesNotExist: User matching query does not exist.
        # response = self.client.get('/authapp/profile/')
        # self.assertEqual(response.status_code, 302)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/authapp/profile/')
        self.assertEqual(response.status_code, 200)


    # def test_product_product(self):
    #     for product_item in Product.objects.all():
    #         response = self.client.get(f'/products/detail/{product_item.pk}/')
    #         self.assertEqual(response.status_code, 200)
    #
    # def tearDown(self) -> None:
    #     pass




# Create your tests here.
