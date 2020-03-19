# import pytest
# from django.conf import settings
# from django.urls import reverse, resolve
#
# pytestmark = pytest.mark.django_db
#
#
# def test_detail(user: settings.AUTH_USER_MODEL):
#     assert (
#         reverse("users:detail", kwargs={"username": user.username})
#         == f"/users/{user.username}/"
#     )
#     assert resolve(f"/users/{user.username}/").view_name == "users:detail"
#
#
# def test_update():
#     assert reverse("users:update") == "/users/~update/"
#     assert resolve("/users/~update/").view_name == "users:update"
#
#
# def test_redirect():
#     assert reverse("users:redirect") == "/users/~redirect/"
#     assert resolve("/users/~redirect/").view_name == "users:redirect"
from django.urls import reverse, resolve
from test_plus import TestCase


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user(username='testuser', password='password')

    def test_detail_reverse(self):
        reversed_url = reverse("users:detail", kwargs={"username": self.user.username})
        self.assertEqual(reversed_url, f"/users/{self.user.username}/")

    def test_detail_resolve(self):
        resolve_url = resolve(f"/users/{self.user.username}/").view_name
        self.assertEqual(resolve_url, "users:detail")

    def test_update_reverse(self):
        reversed_url = reverse("users:update")
        self.assertEqual(reversed_url, "/users/~update/")

    def test_update_resolve(self):
        resolve_url = resolve("/users/~update/").view_name
        self.assertEqual(resolve_url, "users:update")

    def test_redirect_reverse(self):
        reversed_url = reverse("users:redirect")
        self.assertEqual(reversed_url, "/users/~redirect/")

    def test_redirect_resolve(self):
        resolve_url = resolve("/users/~redirect/").view_name
        self.assertEqual(resolve_url, "users:redirect")
