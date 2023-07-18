
```py
request = {
    model="",            # (r) (str)
    prompt="",           # (r) (str | [])
    max_tokens=16,       #     (int)         (default 16)
    temperature=1,       #     (int | float) (default 1)       (0 - 2)
    top_p=1,             #     (int | float) (default 1)       (0 - 2)
    n=1,                 #     (int)         (default 1)
    stream=False,        #     (bool)        (default False)
    logprobs=None,       #     (int | Null)  (default Null)    (0 - 5)
    echo=False,          #     (bool)        (default False)
    stop=None,           #     (str | [])    (default Null)
    presence_penalty=0,  #     (int | float) (default 0)       (-2.0 - 2.0)
    frequency_penalty=0, #     (int | float) (default 0)       (-2.0 - 2.0)
    best_of=1,           #     (int)         (default 1)
    logit_bias=None,     #     (map | None)  (default None) ex.{"50256": -100}
    user=""              #     (str)
}
```
