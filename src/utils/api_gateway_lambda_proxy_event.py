import json

def execute(_event, _context, controller):
    response = controller.proxy_handler(_event, _context)
    body = response.get('body')
    return json.loads(body)

class LambdaEventMock:
    def __init__(self, organization, username):
        self.organization = organization
        self.username = username

    def body(self, method, path, queryStringParameters={}, body={}):
        return {
            "resource": path,
            "path": path,
            "httpMethod": method,
            "headers": {
                "accept": "application/json, text/plain, */*",
                "Authorization": "Bearer UyQkyHjlaDWgTc...",
                "content-type": "application/json",
                "Host": "localhost",
                "origin": "https://localhost",
                "referer": "https://localhost/",
                "X-Forwarded-Port": "443",
                "X-Forwarded-Proto": "https"
            },
            "multiValueHeaders": {
                "accept": [
                    "application/json, text/plain, */*"
                ],
                "Authorization": [
                    "Bearer UyQkyHjlaDWgTc..."
                ],
                "content-type": [
                    "application/json"
                ]
            },
            "queryStringParameters": queryStringParameters,
            "multiValueQueryStringParameters": "",
            "pathParameters": "",
            "stageVariables": "",
            "requestContext": {
                "resourceId": "xxxxx",
                "authorizer": {
                    "claims": {
                        "custom:organization": f"{self.organization}",
                        "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_XXXXXXXX",
                        "phone_number_verified": "true",
                        "cognito:username": f"{self.username}",
                        "event_id": "XXXXXXXXXX",
                        "token_use": "id",
                        "auth_time": "1708114871",
                        "email": "youremail@yourcompany"
                    }
                },
                "resourcePath": path,
                "httpMethod": "POST",
                "requestTime": "29/Feb/2024:20:21:37 +0000",
                "path": path,
                "protocol": "HTTP/1.1",
                "stage": "dev",
                "domainPrefix": "api",
                "requestTimeEpoch": 1708114897280,
                "requestId": "xxxxx-xxxxx-xxxxx",
                "identity": {},
                "domainName": "localhost",
                "deploymentId": "xxxxxx",
                "apiId": "xxxxxx"
            },
            "body": json.dumps(body),
            "isBase64Encoded": False
        }

class LambdaContextMock:
    def __init__(self):
        self.function_name = 'sampleLambdaFunction'
        self.function_version = '1'
        self.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:sampleLambdaFunction'
        self.memory_limit_in_mb = '128'
        self.aws_request_id = 'unique-request-id'
        self.log_group_name = '/aws/lambda/sampleLambdaFunction'
        self.log_stream_name = '2024/02/11/[$LATEST]unique-log-stream-name'
        self.identity = None
        self.client_context = None
        self.deadline_ms = 30000  # Mock example, you might want to calculate this

    def get_remaining_time_in_millis(self):
        # Mock implementation, adjust accordingly
        return self.deadline_ms