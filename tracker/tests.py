from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ExpenseIncome
from decimal import Decimal


class UserRegistrationTest(APITestCase):
    def test_user_registration_success(self):
        """Test successful user registration"""
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'Testpass123!',
            'password2': 'Testpass123!',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'Testpass123!',
            'password2': 'Differentpass123!',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass123!',
            email='test@example.com'
        )

    def test_login_success(self):
        """Test successful login"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'Testpass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ExpenseIncomeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass123!'
        )

    def test_expense_creation(self):
        """Test creating an expense record"""
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title='Test Expense',
            amount=Decimal('100.00'),
            transaction_type='debit',
            tax=Decimal('10.00'),
            tax_type='flat'
        )
        self.assertEqual(expense.title, 'Test Expense')
        self.assertEqual(expense.total, Decimal('110.00'))

    def test_income_creation(self):
        """Test creating an income record"""
        income = ExpenseIncome.objects.create(
            user=self.user,
            title='Test Income',
            amount=Decimal('1000.00'),
            transaction_type='credit',
            tax=Decimal('5.00'),
            tax_type='percentage'
        )
        self.assertEqual(income.title, 'Test Income')
        self.assertEqual(income.total, Decimal('1050.00'))  # 1000 + 5%

    def test_flat_tax_calculation(self):
        """Test flat tax calculation"""
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title='Flat Tax Test',
            amount=Decimal('100.00'),
            transaction_type='debit',
            tax=Decimal('10.00'),
            tax_type='flat'
        )
        self.assertEqual(expense.total, Decimal('110.00'))

    def test_percentage_tax_calculation(self):
        """Test percentage tax calculation"""
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title='Percentage Tax Test',
            amount=Decimal('100.00'),
            transaction_type='debit',
            tax=Decimal('10.00'),
            tax_type='percentage'
        )
        self.assertEqual(expense.total, Decimal('110.00'))  # 100 + 10%

    def test_zero_tax_calculation(self):
        """Test zero tax calculation"""
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title='Zero Tax Test',
            amount=Decimal('100.00'),
            transaction_type='debit',
            tax=Decimal('0.00'),
            tax_type='flat'
        )
        self.assertEqual(expense.total, Decimal('100.00'))


class ExpenseIncomeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass123!'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_expense(self):
        """Test creating an expense via API"""
        url = reverse('expense-list')
        data = {
            'title': 'API Test Expense',
            'amount': '100.00',
            'transaction_type': 'debit',
            'tax': '10.00',
            'tax_type': 'flat'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpenseIncome.objects.count(), 1)
        self.assertEqual(response.data['total'], 110.0)

    def test_list_expenses(self):
        """Test listing expenses"""
        # Create test expenses
        ExpenseIncome.objects.create(
            user=self.user,
            title='Expense 1',
            amount=Decimal('100.00'),
            transaction_type='debit'
        )
        ExpenseIncome.objects.create(
            user=self.user,
            title='Expense 2',
            amount=Decimal('200.00'),
            transaction_type='debit'
        )

        url = reverse('expense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_expense(self):
        """Test retrieving a single expense"""
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title='Test Expense',
            amount=Decimal('100.00'),
            transaction_type='debit'
        )
        url = reverse('expense-detail', args=[expense.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Expense')

    def test_update_expense(self):
        """Test updating an expense"""
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title='Original Title',
            amount=Decimal('100.00'),
            transaction_type='debit'
        )
        url = reverse('expense-detail', args=[expense.id])
        data = {
            'title': 'Updated Title',
            'amount': '150.00',
            'transaction_type': 'debit'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_expense(self):
        """Test deleting an expense"""
        expense = ExpenseIncome.objects.create(
            user=self.user,
            title='Test Expense',
            amount=Decimal('100.00'),
            transaction_type='debit'
        )
        url = reverse('expense-detail', args=[expense.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExpenseIncome.objects.count(), 0)


class PermissionTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='Testpass123!'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='Testpass123!'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='Adminpass123!',
            email='admin@example.com'
        )

    def test_user_cannot_access_other_user_expense(self):
        """Test that a user cannot access another user's expense"""
        # Create expense for user1
        expense = ExpenseIncome.objects.create(
            user=self.user1,
            title='User1 Expense',
            amount=Decimal('100.00'),
            transaction_type='debit'
        )

        # Try to access with user2
        self.client.force_authenticate(user=self.user2)
        url = reverse('expense-detail', args=[expense.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_access_all_expenses(self):
        """Test that superuser can access all expenses"""
        # Create expenses for both users
        expense1 = ExpenseIncome.objects.create(
            user=self.user1,
            title='User1 Expense',
            amount=Decimal('100.00'),
            transaction_type='debit'
        )
        expense2 = ExpenseIncome.objects.create(
            user=self.user2,
            title='User2 Expense',
            amount=Decimal('200.00'),
            transaction_type='debit'
        )

        # Access with superuser
        self.client.force_authenticate(user=self.superuser)
        
        # Should be able to access both
        url1 = reverse('expense-detail', args=[expense1.id])
        response1 = self.client.get(url1)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        url2 = reverse('expense-detail', args=[expense2.id])
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_access_own_expenses(self):
        """Test that user can access their own expenses"""
        expense = ExpenseIncome.objects.create(
            user=self.user1,
            title='My Expense',
            amount=Decimal('100.00'),
            transaction_type='debit'
        )

        self.client.force_authenticate(user=self.user1)
        url = reverse('expense-detail', args=[expense.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_access_expenses(self):
        """Test that unauthenticated users cannot access expenses"""
        expense = ExpenseIncome.objects.create(
            user=self.user1,
            title='Test Expense',
            amount=Decimal('100.00'),
            transaction_type='debit'
        )

        url = reverse('expense-detail', args=[expense.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PaginationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass123!'
        )
        self.client.force_authenticate(user=self.user)

    def test_pagination(self):
        """Test that responses are paginated"""
        # Create more than 10 expenses (default page size)
        for i in range(15):
            ExpenseIncome.objects.create(
                user=self.user,
                title=f'Expense {i}',
                amount=Decimal('100.00'),
                transaction_type='debit'
            )

        url = reverse('expense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 10)  # Default page size
        self.assertEqual(response.data['count'], 15)
