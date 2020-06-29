"""This program creates Flask web server and registers a handler for
each MODULE_NAME:FUNCTION_NAME pair passed in through positional
arguments. The module and function names are used to derive the
handler name. As an example, if the module name is "my.module" and the
function name is "my_function", the handler will be registered at
"/my_module__my_function".
"""
import logging
import os
import sys
import textwrap

import flask


logging.basicConfig(level=logging.INFO)


app = flask.Flask(__name__)


def _parse_args():
    if len(sys.argv) < 2:
        raise ValueError('At least one argument must be provided.')
    result = []
    for arg in sys.argv[1:]:
        parts = tuple(arg.split(':'))
        if len(parts) != 2:
            raise ValueError(
                f'Each argument must follow the format MODULE_NAME:FUNCTION_NAME; '
                'received: {arg}')
        if parts in result:
            raise ValueError(f'Duplicate argument: {arg}')
        result.append(parts)
    return result


def _get_handler_name(module, function):
    module = module.replace('.', '_')
    return f'{module}__{function}'


def _create_handler(module, function):
    handler_name = _get_handler_name(module, function)
    exec(textwrap.dedent(f"""\
        import {module}

        @app.route('/{handler_name}', methods=['POST'])
        def {handler_name}():
            retval = {module}.{function}()
            if isinstance(retval, str):
                return retval
            else:
                return ''
        """), globals(), globals())
    logging.info('Added handler: /%s', handler_name)


def _init():
    for module, function in _parse_args():
        _create_handler(module, function)


_init()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
