
def memory(response: str, request: str) -> str:
    _response = response
    _request = request
    formatted_request = None
    rs = [ # response sections
        "You asked me ",
        "You told me ",
        "You said ",
        "You asked ",
        " and I'm responding with ",
        " What do you say next?"
    ]
    is_question = response.endswith('?')
    if is_question:
        formatted_request = f"{rs[0]}{_response}{rs[4]}{_request}{rs[5]}" 
    else:
        formatted_request = f"{rs[1]}{_response}{rs[4]}{_request}{rs[5]}"
    return str(formatted_request)
