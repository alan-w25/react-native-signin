from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError 
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


# Create your tests here.

class UserModelTests(TestCase): 
    
    def setUp(self): 
        self.User = get_user_model() 
        self.user_email = 'test@example.com'
        self.user_username = 'testuser'
        self.user_password = 'password123!'
        
    def test_create_user(self): 
        user = self.User.objects.create_user(
            email = self.user_email, 
            username=self.user_username, 
            password=self.user_password
        )
        
        self.assertEqual(user.email, self.user_email) 
        self.assertEqual(user.username, self.user_username)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self): 
        admin_user = self.User.objects.create_superuser(
            email = self.user_email, 
            username=self.user_username, 
            password=self.user_password
        )
        
        self.assertEqual(admin_user.email, self.user_email) 
        self.assertEqual(admin_user.username, self.user_username)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_email_uniqueness(self): 
        self.User.objects.create_user(
            email = self.user_email, 
            username=self.user_username, 
            password=self.user_password
        )
        
        with self.assertRaises(IntegrityError): 
            self.User.objects.create_user(
                email = self.user_email, 
                username="anotheruserame", 
                password=self.user_password
            )
    
    def test_username_uniqueness(self): 
        self.User.objects.create_user(
            email = self.user_email, 
            username=self.user_username, 
            password=self.user_password
        )
        
        with self.assertRaises(IntegrityError): 
            self.User.objects.create_user(
                email = "another@example.com", 
                username=self.user_username, 
                password=self.user_password
                )
    def test_password_hashing(self): 
        user = self.User.objects.create_user(
            email = self.user_email, 
            username=self.user_username, 
            password=self.user_password
        )
        
        self.assertNotEqual(user.password, self.user_password)
        self.assertTrue(user.check_password(self.user_password))
        

User = get_user_model()
class UserRegistrationTests(TestCase): 
    
    def setUp(self): 
        self.client = APIClient() 
        self.registration_url = reverse('register')
    
    def test_register_user_success(self): 
        payload = {
            'email':'test@example.com', 
            'username':'testuser',
            'password':'password123!', 
            'password2':'password123!'
        }
        
        response = self.client.post(self.registration_url, payload) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data) 
        self.assertIn('username', response.data)
        self.assertNotIn('password', response.data)
        self.assertTrue(User.objects.filter(email=payload['email']).exists())
    
    def test_register_user_password_mismatch(self): 
        payload = {
            'email':'test2@example.com', 
            'username':'testuser2',
            'password':'password123', 
            'password2':'password456'
        }
        
        response = self.client.post(self.registration_url, payload) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        self.assertIn('password', response.data) 
        self.assertFalse(User.objects.filter(email='test2@example.com').exists())
        
    
    def test_register_user_missing_field(self): 
        payload = {
            'email':'test3@example.com', 
            'password':'password123', 
            'password2':'password123'
        }
        
        response = self.client.post(self.registration_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertFalse(User.objects.filter(email='test3@example.com').exists())
        

class UserLoginTests(TestCase): 
    
    def setUp(self): 
        self.client = APIClient() 
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email='test@example.com', 
            username='testuser',
            password='password123')
        
    def test_login_success(self): 
        response = self.client.post(self.login_url, {
            'email':'test@example.com', 
            'password':'password123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self): 
        response = self.client.post(self.login_url, {
            'email':'test@example.com', 
            'password':'wrongpassword'
        })
        print(response)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
        
    def test_login_missing_fields(self): 
        response = self.client.post(self.login_url, {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh',response.data)
    
    def test_refresh_tokens(self): 
        login_response = self.client.post(self.login_url, {
            'email':'test@example.com', 
            'password':'password123',
        }) 
        refresh_token = login_response.data['refresh']
        
        refresh_url = reverse('token_refresh')
        response = self.client.post(refresh_url, {
            'refresh':refresh_token,
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)