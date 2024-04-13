# from dotenv import load_dotenv
#
# load_dotenv()

import pytest

from src.utils.api_gateway_lambda_proxy_event import LambdaContextMock, LambdaEventMock, execute
from src.api import users as user_controller

event = LambdaEventMock('myorg', 'myusername')

# @pytest.fixture(scope="session", autouse=True)
# def populate_data():
#     user_data_populating_method()
#
#     yield
#
#    user_data_cleanup_method()


@pytest.fixture(scope="session", autouse=True)
def created_user():
    return execute(event.body('POST', '/user',
                          {},
                          {
                              "organization": event.organization,
                              "name": 'NEW USER NAME'
                          }), LambdaContextMock(), user_controller)

@pytest.fixture(scope="session", autouse=True)
def all_users():
    return execute(event.body('GET', '/users'), LambdaContextMock(), user_controller)

# @pytest.fixture(scope="session", autouse=True)
# def find_user(created_user):
#     user_id = created_user.get('user_id')
#     return execute(event.body('GET', '/user', {"user_id": user_id}), LambdaContextMock(), user_controller)
#
# @pytest.fixture(scope="session", autouse=True)
# def updated_user(created_user):
#     user_id = created_user.get('user_id')
#     return execute(event.body('PUT', '/user',
#                           {"user_id": user_id},
#                           {
#                              "name": "UPDATED USER NAME"
#                           }
#                           ), LambdaContextMock(), user_controller)
#
#
# @pytest.fixture(scope="session", autouse=True)
# def deleted_user(new_invoice):
#     return execute(event.body('DELETE', '/user',
#                       {
#                           "invoice_id": new_invoice.get('invoices'),
#                           "expand": "line_items",
#                       }
#                       ), LambdaContextMock(), user_controller)



class TestUserApiController:
    def test_create_user(self, created_user):
        assert 'body' in created_user



    def test_get_all_users(self, all_users):
        assert 'data' in all_users