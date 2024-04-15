import base64
import json
from http import HTTPStatus

from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig, Response
from aws_lambda_powertools.event_handler.exceptions import (BadRequestError, InternalServerError)
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit, MetricResolution
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service='users_service_api')
tracer = Tracer(service='users_service_api')
metrics = Metrics(service='users_service_api', namespace='user_service')
metrics.set_default_dimensions(environment="dev")

cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayRestResolver(cors=cors_config)


@dataclass
class User:
    user_id: str
    username: str
    full_name: str


@app.post("/user")
@tracer.capture_method
def create_user():
    body = app.current_event.json_body
    if body is None:
        raise BadRequestError("Missing required parameter: body")

    if app.current_event.get('isBase64Encoded', False):
        body = base64.b64decode(body).decode('utf-8', errors='ignore')

    try:
        user = User(**body)
    except TypeError as e:
        raise BadRequestError(f"Missing required parameter or wrong data type {e}") from e

    logger.info(f"user-created: {body}")

    response_data = {"message": "success", "action": "user-created", "user_id": "101", "data": user.__dict__}

    logger.debug(response_data)
    metrics.add_metric(name="CreatedUser", unit=MetricUnit.Count, value=1, resolution=MetricResolution.High)
    metrics.add_metadata(key="user_id", value=f"{uuid4()}")

    return Response(status_code=HTTPStatus.OK.value, content_type="application/json", body=json.dumps(response_data), )


@app.put("/user")
@tracer.capture_method
def update_user():
    user_id = app.current_event.get_query_string_value(name="user_id")

    body = app.current_event.json_body

    if app.current_event.get('isBase64Encoded', False):
        body = base64.b64decode(body).decode('utf-8', errors='ignore')

    try:
        response_data = {"user_id": "101"}
    except Exception as e:
        metadata = {"path": app.current_event.path, "query_strings": app.current_event.query_string_parameters}
        logger.error(f"Cannot create user_id: {e}", extra=metadata)
        raise InternalServerError("Cannot create user_id") from e

    logger.info(f"user-updated: {user_id} {body}")
    metrics.add_metric(name="UpdatedUser", unit=MetricUnit.Count, value=1, resolution=MetricResolution.High)
    metrics.add_metadata(key="user_id", value=user_id)
    tracer.put_annotation(key="user_id", value=user_id)

    return response_data


@app.get("/users")
@tracer.capture_method
def find_users():
    user_id = app.current_event.get_query_string_value(name="user_id", default_value="")

    if user_id:
        if len(user_id) < 3:
            metadata = {"path": app.current_event.path, "query_strings": app.current_event.query_string_parameters}
            logger.error(f"Error finding user, user_id len should be > 3", extra=metadata)
            raise BadRequestError(
                "Error finding user, user_id len should be > 3")  # return Response(  #     status_code=422,  #     content_type=content_types.APPLICATION_JSON,  #     body="Error finding user, user_id len should be > 3",  # )

        try:
            response_data = {"user_id": "101", "username": "one o one"}
        except TypeError as e:
            metadata = {"path": app.current_event.path, "query_strings": app.current_event.query_string_parameters}
            logger.error(f"Missing required parameter or wrong data type: {e}", extra=metadata)
            raise InternalServerError("Missing required parameter or wrong data type") from e

        logger.info(f"Find user_id: {user_id}")
        metrics.add_metric(name="FindUser", unit=MetricUnit.Count, value=1, resolution=MetricResolution.High)
        metrics.add_metadata(key="user_id", value=user_id)
        tracer.put_annotation(key="user_id", value=user_id)

        return Response(status_code=HTTPStatus.OK.value, content_type="application/json",
                        body=json.dumps(response_data), )

    try:
        response_data = {"count": "101",
                         "data": [{"user_id": "101", "username": "one o one"},
                                  {"user_id": "102", "username": "one o two"}]}
    except TypeError as e:
        metadata = {"path": app.current_event.path, "query_strings": app.current_event.query_string_parameters}
        logger.error(f"Missing required parameter or wrong data type: {e}", extra=metadata)
        raise InternalServerError("Missing required parameter or wrong data type") from e

    logger.info(f"Find all users")
    metrics.add_metric(name="FindUsers", unit=MetricUnit.Count, value=1, resolution=MetricResolution.High)
    metrics.add_metadata(key="count", value=response_data.get('count'))
    tracer.put_annotation(key="count", value=response_data.get('count'))

    return Response(status_code=HTTPStatus.OK.value, content_type="application/json", body=json.dumps(response_data), )


@app.delete("/user")
@tracer.capture_method
def delete_user():
    user_id = app.current_event.get_query_string_value(name="user_id", default_value="")

    try:
        response_data = {"message": "success", "action": "user-deleted", "user_id": f"{uuid4()}", "username": "one o one"}
    except Exception as e:
        metadata = {"path": app.current_event.path, "query_strings": app.current_event.query_string_parameters}
        logger.error(f"Missing required parameter or wrong data type: {e}", extra=metadata)
        raise InternalServerError("Missing required parameter or wrong data type") from e

    logger.info(f"Delete user_id: {user_id}")
    metrics.add_metric(name="DeleteUser", unit=MetricUnit.Count, value=1, resolution=MetricResolution.High)
    metrics.add_metadata(key="user_id", value=response_data.get('user_id'))
    tracer.put_annotation(key="user_id", value=response_data.get('user_id'))

    return Response(status_code=HTTPStatus.OK.value, content_type="application/json", body=json.dumps(response_data), )


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def proxy_handler(event, context: LambdaContext):
    print("*" * 88)
    print("-" * 88)
    return app.resolve(event, context)
