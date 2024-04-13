from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/user")
def create():
    return {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json"
      },
      "body": "{\"key\": \"value\"}",
      "isBase64Encoded": False
    }

@app.put("/user")
def create():
    return {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json"
      },
      "body": "{\"key\": \"value\"}",
      "isBase64Encoded": False
    }

@app.get("/users")
def create():
    return {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json"
      },
      "body": "{\"key\": \"value\"}",
      "isBase64Encoded": False
    }

@app.delete("/user")
def create():
    return {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json"
      },
      "body": "{\"key\": \"value\"}",
      "isBase64Encoded": False
    }


@logger.inject_lambda_context()
def proxy_handler(event, context: LambdaContext):
    return app.resolve(event, context)