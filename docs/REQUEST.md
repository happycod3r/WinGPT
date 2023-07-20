# Requests
## Chat
```py
request = {
    engine="",            # (r) (str)
    prompt="",           # (r) (str | [])
    max_tokens=16,       #     (int)         (default 16)
    temperature=1,       #     (int | float) (default 1)       (0 - 2)
    n=1,                 #     (int)         (default 1)
    stream=False,        #     (bool)        (default False)
    echo=False,          #     (bool)        (default False)
    stop=None,           #     (str | [])    (default Null)
    presence_penalty=0,  #     (int | float) (default 0)       (-2.0 - 2.0)
    frequency_penalty=0, #     (int | float) (default 0)       (-2.0 - 2.0)
    best_of=1,           #     (int)         (default 1)
    timeout=None         #     (int)         (default None
}
```
