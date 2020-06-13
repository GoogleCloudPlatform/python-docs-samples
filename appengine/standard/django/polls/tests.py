from django.test import Client, TestCase  # noqa: 401


class PollViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert 'Hello, world' in str(response.content)
