# import pytest
# from django.conf import settings
# from django.test import RequestFactory
#
# from test.users.views import UserRedirectView, UserUpdateView
#
# pytestmark = pytest.mark.django_db
#
#
# class TestUserUpdateView:
#     """
#     TODO:
#         extracting view initialization code as class-scoped fixture
#         would be great if only pytest-django supported non-function-scoped
#         fixture db access -- this is a work-in-progress for now:
#         https://github.com/pytest-dev/pytest-django/pull/258
#     """
#
#     def test_get_success_url(
#         self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
#     ):
#         view = UserUpdateView()
#         request = request_factory.get("/fake-url/")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_success_url() == f"/users/{user.username}/"
#
#     def test_get_object(
#         self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
#     ):
#         view = UserUpdateView()
#         request = request_factory.get("/fake-url/")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_object() == user
#
#
# class TestUserRedirectView:
#     def test_get_redirect_url(
#         self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
#     ):
#         view = UserRedirectView()
#         request = request_factory.get("/fake-url")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_redirect_url() == f"/users/{user.username}/"
from test_plus import TestCase
from django.test import RequestFactory
from test.users.views import UserUpdateView, UserRedirectView


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.make_user(username='testuser', password='password')


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        super(TestUserUpdateView, self).setUp()
        self.view = UserUpdateView()
        request = self.factory.get('/fake-url')
        request.user = self.user
        self.view.request = request

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), f"/users/{self.user.username}/")

    def test_get_object(self):
        self.assertEqual(self.view.get_object(), self.user)


class TestUserRedirectView(BaseUserTestCase):

    def setUp(self):
        super(TestUserRedirectView, self).setUp()
        self.view = UserRedirectView()
        request = self.factory.get('/fake-url')
        request.user = self.user
        self.view.request = request

    def test_get_redirect_url(self):
        self.assertEqual(self.view.get_redirect_url(), f"/users/{self.user.username}/")

