#!/usr/bin/env python
import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap


_SERVER_TEMPLATE = """
import logging
import os

import flask

{imports}


logging.basicConfig(level=logging.INFO)


app = flask.Flask(__name__)


{handlers}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
"""


_DATA_DIR = os.path.dirname(__file__)
_DATA_FILES = (
    'Dockerfile',
    '.dockerignore',
)


_DEPS = (
    'flask',
    'gunicorn',
)


class CronifyError(Exception):
    pass


def _get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--keep-temp-dir', action='store_true',
                        default=False,
                        help='If provided, the temporary directory is not deleted.')

    return parser.parse_args()


def _copy_files(dest):
    shutil.copytree(src=os.getcwd(), dst=dest, dirs_exist_ok=True)
    for f in _DATA_FILES:
        shutil.copy(src=os.path.join(_DATA_DIR, f), dst=dest)


def _write_requirements(dest):
    with open(os.path.join(dest, 'requirements.txt'), 'a') as f:
        f.writelines(f'{dep}\n' for dep in _DEPS)


def _get_configs():
    try:
        with open(os.path.join(os.getcwd(), 'cronify.json')) as f:
            return json.load(f)
    except FileNotFoundError:
        raise CronifyError('Directory is missing cronify.json.')


def _get_handler_name(module, function):
    module = module.replace('.', '_')
    return f'{module}__{function}'


def _generate_server(configs):
    imports = []
    handlers = []
    for config in configs['functions']:
        module = config['module']
        function = config['function']
        handler_name = _get_handler_name(module=module, function=function)

        imports.append(f'import {module}\n')
        handlers.append(textwrap.dedent(f"""\
            @app.route('/{handler_name}', methods=['POST'])
            def {handler_name}():
                retval = {module}.{function}()
                if isinstance(retval, str):
                    return retval
                else:
                    return ''
            """))

    return _SERVER_TEMPLATE.format(
        imports='\n'.join(imports), handlers='\n'.join(handlers))


def _write_server(configs, dest):
    server = _generate_server(configs)
    with open(os.path.join(dest, 'cronify_entry.py'), 'w') as f:
        f.write(server)


def _deploy(configs, dest):
    project_id = configs['project-id']
    region = configs['region']
    image_name = f'gcr.io/{project_id}/{os.path.basename(os.getcwd())}'

    commands = [
        [
            'gcloud',
            f'--project={project_id}',
            'builds',
            'submit',
            f'--tag={image_name}',
        ],
        [
            'gcloud',
            f'--project={project_id}',
            'run',
            'deploy',
            f'--region={region}',
            f'--image={image_name}',
            '--platform=managed',
        ]
    ]

    for command in commands:
        output = subprocess.run(command,
                                cwd=dest,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        sys.stderr.write(output.stdout.decode('utf'))
        if output.returncode != 0:
            raise CronifyError('gcloud command failed.')


def main():
    logging.basicConfig(level=logging.INFO)
    args = _get_args()

    dest = tempfile.mkdtemp(prefix='cronify-')
    try:
        logging.info('Files will be staged in %s', dest)
        configs = _get_configs()
        _write_server(configs, dest)

        _copy_files(dest)
        _write_requirements(dest)

        _deploy(configs, dest)

    except CronifyError as e:
        sys.stderr.write(str(e))
        sys.stderr.write('\n')
        sys.exit(1)

    finally:
        if not args.keep_temp_dir:
            shutil.rmtree(dest)


if __name__ == '__main__':
    main()
