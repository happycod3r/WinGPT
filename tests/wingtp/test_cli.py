import unittest
import cli
import modules.debug as dbg

_cli = cli.OpenAIInterface()

_data = [
    _cli.api_key_path, 
    _cli.api_key, 
    _cli.api_base, 
    _cli.api_type, 
    _cli.api_version,
    _cli.organization, 
    _cli.engine, 
    _cli.user_defined_filename,
    _cli.jsonl_data_file,
    _cli.stop_list,
    _cli.use_stop_list, 
    _cli.echo, 
    _cli.stream, 
    _cli.save_chat,
    _cli.temperature, 
    _cli.frequency_penalty, 
    _cli.presence_penalty, 
    _cli.response_count,
    _cli.response_token_limit, 
    _cli.best_of, 
    _cli.request_type,
    _cli.request,
    _cli.timeout
] 
dbg.out(_data)
