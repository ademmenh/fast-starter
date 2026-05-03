from http import HTTPStatus

def get_error_schema(status_code: int, message_type: str = "string"):
    properties = {
        "error": {"type": "string", "example": HTTPStatus(status_code).name},
        "statusCode": {"type": "integer", "example": status_code},
        "message": {"type": message_type},
    }
    if message_type == "array":
        properties["message"] = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "loc": {"type": "array", "items": {"type": "string"}},
                    "msg": {"type": "string"},
                    "input": {"type": "object"},
                },
            },
        }
    return {"type": "object", "properties": properties}

def custom_openapi(openapi_schema: dict):
    # ── Security Schemes ──────────────────────────────────────────────────────────
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}
    
    openapi_schema["components"]["securitySchemes"].update({
        "CookieAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token"
        },
        "RefreshToken": {
            "type": "apiKey",
            "in": "cookie",
            "name": "refresh_token"
        }
    })

    error_codes = [400, 401, 403, 404, 422, 500]
    for path in openapi_schema["paths"].values():
        for method in path.values():
            responses = method.get("responses", {})
            for code in error_codes:
                str_code = str(code)
                if code == 422:
                    msg_type = "array"
                elif code == 500:
                    msg_type = None
                else:
                    msg_type = "string"
                schema = get_error_schema(code, msg_type)
                
                if str_code not in responses:
                    responses[str_code] = {
                        "description": HTTPStatus(code).phrase,
                        "content": {"application/json": {"schema": schema}}
                    }
                else:
                    responses[str_code]["content"] = {
                        "application/json": {"schema": schema}
                    }
            method["responses"] = responses

    return openapi_schema

