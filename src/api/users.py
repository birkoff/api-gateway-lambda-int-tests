import base64

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/user")
def create():
    body = app.current_event.get('body')
    if app.current_event.get('isBase64Encoded', False):
        body = base64.b64decode(body).decode('utf-8', errors='ignore')

    logger.info(f"user-created: {body}")

    response_data = {
        "message": "success",
        "action": "user-created",
        "user_id": "101"
    }

    return response_data



@app.put("/user")
def update():
    query_string = app.current_event.get('queryStringParameters')
    user_id = query_string.get('user_id')

    body = app.current_event.get('body')

    if app.current_event.get('isBase64Encoded', False):
        body = base64.b64decode(body).decode('utf-8', errors='ignore')

    logger.info(f"user-updated: {user_id} {body}")

    response_data = {
        "message": "success",
        "action": "user-updated",
        "user_id": "101"
    }

    return response_data


@app.get("/users")
def find():
    query_string = app.current_event.get('queryStringParameters')
    user_id = query_string.get('user_id', None)

    if user_id:
        logger.info(f"Find user_id: {user_id}")
        response_data = {
            "user_id": "101",
            "username": "one o one"
        }
        return response_data

    logger.info(f"Find all users")
    response_data = {
        "count": "101",
        "data": [
            {
                "user_id": "101",
                "username": "one o one"
            },
            {
                "user_id": "102",
                "username": "one o two"
            }
        ]
    }
    return response_data


@app.delete("/user")
def delete():
    query_string = app.current_event.get('queryStringParameters')
    user_id = query_string.get('user_id')

    logger.info(f"Delete user_id: {user_id}")
    response_data = {
        "message": "success",
        "action": "user-deleted",
        "user_id": "101",
        "username": "one o one"
    }
    return response_data


@logger.inject_lambda_context()
def proxy_handler(event, context: LambdaContext):
    return app.resolve(event, context)
