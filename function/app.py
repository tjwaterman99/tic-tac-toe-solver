import json
from model.api import predict, DEFAULT_MODEL_PATH
from model.qtable import QTable


qtable = QTable.from_json(DEFAULT_MODEL_PATH)


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "Thu, 01 Jan 1970 00:00:00 GMT"        
    }    

    if event.get('httpMethod') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": ""
        }

    try:
        body = json.loads(event.get("body"))
        board = body["board"]
        player = body["player"]
        prediction = predict(board=board, player=player, qtable=qtable)
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                **cors_headers,
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e),
                "success": False
            })
        }

    return {
        "statusCode": 200,
        "headers": cors_headers,        
        "body": json.dumps(prediction),
    }
