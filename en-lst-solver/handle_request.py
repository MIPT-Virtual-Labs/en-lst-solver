import solver_dummy


def handle_request(request_json):

    response = {"status": "failed", "info": None}

    if "function" not in request_json:
        response["info"] = "Missing `function` argument"
        return response
    function = request_json["function"]

    if "x" not in request_json:
        response["info"] = f"Missing `x` argument"
        return response
    x = request_json["x"]

    if function == "square":
        result = solver_dummy.functions.square(x)
    elif function == "cube":
        result = solver_dummy.functions.cube(x)
    elif function == "factorial":
        result = solver_dummy.factorial(x)
    else:
        response["info"] = f"Unknown function: {function}"
        return response

    response["result"] = result
    response["status"] = "success"

    return response
