from fabric import Connection, task
from deploy_tools import fabfile


HOST = 'czekaltudlugo@s0.small.pl'
PYTHON_LOC = '~/venvs/tdd-django/bin/python'


def _get_superlists_dir(domain):
    return f'/home/czekaltudlugo/domains/{domain}/public_python'


def reset_database(domain):
    c = Connection(HOST)
    superlists_dir = _get_superlists_dir(domain)
    with c.cd(superlists_dir):
        c.run(f'{PYTHON_LOC} manage.py flush --noinput')


def create_session_on_server(domain, email):
    c = Connection(HOST)
    superlists_dir = _get_superlists_dir(domain)
    with c.cd(superlists_dir):
        with c.prefix('source .env'):
            session_key = c.run(f'{PYTHON_LOC} manage.py create_session {email}')
            c.close()
            print(session_key)
            return session_key.stdout.strip()
