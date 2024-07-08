import os
import unittest
from app import app, db
from models import User



class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_URI'),

        # Create test database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables in the test database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user_success(self):
        response = self.app.post('/auth/register', json={
            'firstName': 'Synth',
            'lastName': 'Chidi',
            'email': 'synth.chidi@example.com',
            'password': 'password123',
            'phone': '1234567890'
        })

        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')
        self.assertIn('accessToken', data['data'])
        self.assertIn('userId', data['data']['user'])
        self.assertIn('Synth\'s Organisation', data['data']['user']['firstName'] + '\'s Organisation')

    def test_register_user_missing_field(self):
        response = self.app.post('/auth/register', json={
            'firstName': 'Synth',
            'lastName': 'Chidi',
            'email': 'synth.chidi@example.com',
            'phone': '1234567890'
        })
        self.assertEqual(response.status_code, 422)

    def test_register_duplicate_email(self):
        self.app.post('/auth/register', json={
            'userId': 'testuser',
            'firstName': 'Synth',
            'lastName': 'Chidi',
            'email': 'synth.chidi@example.com',
            'password': 'password123',
            'phone': '1234567890'
        })
        response = self.app.post('/auth/register', json={
            'userId': 'testuser2',
            'firstName': 'Mama',
            'lastName': 'Chidi',
            'email': 'synth.chidi@example.com',
            'password': 'password123',
            'phone': '0987654321'
        })
        self.assertEqual(response.status_code, 422)

    def test_login_user_success(self):
        self.app.post('/auth/register', json={
            'userId': 'testuser',
            'firstName': 'Synth',
            'lastName': 'Chidi',
            'email': 'synth.chidi@example.com',
            'password': 'password123',
            'phone': '1234567890'
        })
        response = self.app.post('/auth/login', json={
            'email': 'synth.chidi@example.com',
            'password': 'password123'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertIn('accessToken', data['data'])

    def test_login_user_failure(self):
        response = self.app.post('/auth/login', json={
            'email': 'synth.chidi@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
