
def memory(request: str, response: str) -> str:
    """
    Summary:
        Since models like Davinci don't remember what was said previously we can 
        work around that by provding it with artificial memory. 
        The way this is acomplished is by simply reminding the engine what was 
        previously said in each follow up request. In this way we are essentially 
        providing the memory for the engine. Obviously we could get deep and just 
        keep appending the previous requests and responses to new requests and 
        sending back a record of the entire dialog, but for this example the 
        engine will remember up to onlt the first level of previous requests 
        and response 
    
    Args:
        request (str): Your question or task.
        response (str): The generated response.
    
    """
    _response = response
    _request = request
    formatted_request = None
    rs = [ # response sections
        "You asked me: ",
        "You told me: ",
        "You said: ",
        "You asked: ",
        " and I'm responding with: ",
        " What do you say next?"
    ]
    # For now we'll simply classify every response as either a question or a statement.
    # If it doesn't end with a question mark (?) then consider it a statement.
    is_question = response.endswith('?')
    # If it is a question
    if is_question:
        formatted_request = f" \
            {rs[0]}{_response} \
                {rs[4]}{_request}\n \
                    {rs[5]}" 
            # You asked me: _reponse
                # and I'm responding with: _request
                    # What do you say next?
    else:
        formatted_request = f" \
            {rs[1]}{_response} \
                {rs[4]}{_request}\n \
                    {rs[5]}"
    return str(formatted_request)
