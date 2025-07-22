from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import ResearchAgent  # Assuming you have a model named ResearchAgent
import openai

class ResearchAgentTests(TestCase):
    def setUp(self):
        # Set up any necessary test data here
        self.agent = ResearchAgent.objects.create(
            name="Test Agent",
            description="A test agent for research purposes."
        )

    def test_agent_creation(self):
        """Test that the Research Agent is created correctly."""
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertEqual(self.agent.description, "A test agent for research purposes.")

    def test_agent_str(self):
        """Test the string representation of the Research Agent."""
        self.assertEqual(str(self.agent), "Test Agent")  # Adjust based on your __str__ method

    # Add more tests as needed for your application logic

class ResearchAgentOpenAITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a ResearchAgent for testing
        self.agent = ResearchAgent.objects.create(name='TestAgent', description='Test agent for OpenAI query')

    @patch('openai.chat.completions.create')
    def test_openai_interact_success(self, mock_openai_create):
        # Mock OpenAI response for new API
        class MockChoice:
            class Message:
                content = 'Mocked OpenAI response'
            message = Message()
        mock_openai_create.return_value = type('obj', (object,), {
            'choices': [MockChoice()]
        })()
        payload = {
            'input': 'Test prompt',
            'scope': 'full',
            'agent_id': self.agent.id
        }
        response = self.client.post('/research-agent/research/interact/', payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.data)
        self.assertEqual(response.data['response'], 'Mocked OpenAI response')