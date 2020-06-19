from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user(self):
        """ Test creating a new user with the custom user model"""
        email = 'test@test.com'
        first_name = '       test       '
        last_name = '        user       '
        password = 'TestPass232323232323'
        user = get_user_model().objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        test_first_name = 'Test'
        test_last_name = 'User'
        full_name = f'{test_first_name} {test_last_name}'

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, test_first_name)
        self.assertEqual(user.last_name, test_last_name)
        self.assertEqual(user.get_full_name(), full_name)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_create_staffuser(self):
        """ Test creating a new staffuser with the custom user model"""
        email = 'admin@test.com'
        first_name = 'Staff'
        last_name = 'User'
        full_name = f'{first_name} {last_name}'
        password = 'TestPass232323232323'
        user = get_user_model().objects.create_staffuser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.get_full_name(), full_name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        """ Test creating a new superuser with the custom user model"""
        email = 'superadmin@test.com'
        first_name = 'Super'
        last_name = 'User'
        full_name = f'{first_name} {last_name}'
        password = 'TestPass232323232323'
        user = get_user_model().objects.create_superuser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.get_full_name(), full_name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_validation_create_user(self):
        """ See if regex validation works """
        email = 'test@test.com'
        first_name = '!"#$test'
        last_name = '...ladas12#$#$#$$#$#$#$#$#$user'
        password = 'TestPass232323232323'

        try:
            user = get_user_model().objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
        except ValueError:
            self.assertRaisesMessage(
                ValueError, 'First and last name can only comprise of letters')
