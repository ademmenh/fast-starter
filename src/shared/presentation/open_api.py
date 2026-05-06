from http import HTTPStatus

def get_error_schema(
    status_code: int, 
    message_type: str = "string", 
    error_example: str | None = None,
    message_example: str | None = None
):
    properties = {
        "error": {"type": "string", "example": error_example or HTTPStatus(status_code).name},
        "statusCode": {"type": "integer", "example": status_code},
        "message": {"type": message_type, "example": message_example},
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

    error_codes = [400, 401, 403, 404, 409, 422, 500]
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
                
                # Check if there is a custom description to use as error examples
                error_example = None
                message_example = None
                if str_code in responses:
                    response_obj = responses[str_code]
                    desc = response_obj.get("description", "")
                    
                    if ":" in desc:
                        parts = [s.strip() for s in desc.split(":", 1)]
                        error_example = parts[0]
                        message_example = parts[1]
                    elif desc and desc != HTTPStatus(code).phrase:
                        error_example = desc

                schema = get_error_schema(code, msg_type, error_example, message_example)
                
                if str_code not in responses:
                    responses[str_code] = {
                        "description": HTTPStatus(code).phrase,
                        "content": {"application/json": {"schema": schema}}
                    }
                else:
                    # Update content but KEEP the original description if it exists
                    responses[str_code]["content"] = {
                        "application/json": {"schema": schema}
                    }
            method["responses"] = responses

    return openapi_schema
