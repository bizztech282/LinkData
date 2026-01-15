from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch, MagicMock
from .payhero_api import PayheroService
from .views import initiate_stk
import json

class PayheroServiceTest(TestCase):
    def setUp(self):
        self.service = PayheroService()

    def test_phone_formatting(self):
        """Test that phone numbers are correctly formatted to 254..."""
        self.assertEqual(self.service._format_phone_number("0712345678"), "254712345678")
        self.assertEqual(self.service._format_phone_number("254712345678"), "254712345678")
        self.assertEqual(self.service._format_phone_number("+254712345678"), "254712345678")
        self.assertEqual(self.service._format_phone_number("011 234 5678"), "254112345678")

    @patch('bundles.payhero_api.requests.post')
    def test_initiate_stk_push_success(self, mock_post):
        """Test successful STK push initiation."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "Success", "data": {}}
        mock_post.return_value = mock_response

        # Call service
        result = self.service.initiate_stk_push(
            phone_number="0712345678",
            amount=100,
            reference="REF123",
            description="Test Payment"
        )

        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "STK Push sent successfully.")
        
        # Verify API was called with expected payload
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('json', kwargs)
        self.assertEqual(kwargs['json']['phone_number'], "254712345678")
        self.assertEqual(kwargs['json']['amount'], 100.0)

    @patch('bundles.payhero_api.requests.post')
    def test_initiate_stk_push_failure(self, mock_post):
        """Test failed STK push initiation."""
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        result = self.service.initiate_stk_push(
            phone_number="0712345678",
            amount=100,
            reference="REF123",
            description="Test Payment"
        )

        self.assertFalse(result['success'])
        self.assertIn("API Error", result['message'])

class InitiateStkViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('initiate_stk')

    @patch('bundles.views.PayheroService.initiate_stk_push')
    def test_initiate_stk_view_success(self, mock_initiate):
        """Test the view handles valid POST request correctly."""
        mock_initiate.return_value = {'success': True, 'message': 'Success', 'data': {}}
        
        data = {
            'phone_number': '0712345678',
            'amount': 100
        }
        
        request = self.factory.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        response = initiate_stk(request)
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_initiate_stk_view_missing_data(self):
        """Test the view handles missing data."""
        data = {
            'phone_number': '0712345678'
            # Missing amount
        }
        
        request = self.factory.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        response = initiate_stk(request)
        self.assertEqual(response.status_code, 400)
