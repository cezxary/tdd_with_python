import os

from fabric import Connection, task
import subprocess
import random

REPO_URL = "https://github.com/cezxary/tdd_with_python.git"
SITENAME_PRODUCTION = 'tdd.czekaltudlugo.smallhost.pl'
SITENAME_STAGING = 'tdd-staging.czekaltudlugo.smallhost.pl'
SITENAME_TEST = 'tdd-test.czekaltudlugo.smallhost.pl'


@task
def deploy_production(c):
    _deploy(c, 'production')


@task
def deploy_staging(c):
    _deploy(c, 'staging')


@task
def deploy_test(c):
    _deploy(c, 'test')


def _deploy(c: Connection, site_type):
    print("Please, don't forget to set RECIPIENT_EMAIL_PASSWORD env var")
    target_site = {
        'production': SITENAME_PRODUCTION,
        'test': SITENAME_TEST,
        'staging': SITENAME_STAGING
    }[site_type]

    _create_virtualenv(c)
    _create_devil_python_site(c, site_type, target_site)
    # _update_bash_profile(c, target_site)
    site_folder = f'~/domains/{target_site}/public_python'
    with c.cd(site_folder):
        _get_latest_source(c)
        _update_virtualenv(c)
        _create_or_update_dotenv(c, target_site)
        # _create_or_update_env_var_dotpy(c, target_site)
        with c.prefix('source .env'):
            _update_static_files(c)
            _update_database(c)
            _copy_devil_passenger_config(c)
            _update_passenger_config(c)
            _restart_devil_app(c, target_site)
    c.close()


def _create_virtualenv(c):
    if c.run('~/venvs/tdd-django/bin/python --version').failed:
        c.run(f'python3.8 -m venv ~/venvs/tdd-django')


def _create_devil_python_site(c, site_type, target_site):
    if target_site not in c.run('devil www list').stdout:
        c.run(f'devil www add {target_site} python /usr/home/czekaltudlugo/venvs/tdd-django/bin/python {site_type}')


def _update_bash_profile(c, target_site):
    c.run(f'cat ~/.bash_profile | sed "s#domains/.*/public_python#domains/{target_site}/public_python#"'
          '| tee ~/.bash_profile')


def _get_latest_source(c):
    if c.run(f'ls .git > /dev/null', warn=True).failed:
        c.run(f'rmdir public && rm -rf tmp')
        c.run(f'git clone {REPO_URL} .')
        print('INFO: git repo cloned')
    else:
        c.run('git fetch')
        print('INFO: git repo fetched')
    git_log_return = subprocess.run(['git', 'log', '-n', '1', '--format=%H'], capture_output=True).stdout
    current_commit = git_log_return.decode('utf-8').strip()
    c.run(f'git reset --hard {current_commit}')


def _update_virtualenv(c):
    c.run('~/venvs/tdd-django/bin/pip install `grep -v "selenium" requirements.txt`') # you can modify the command c.run with ( ,warn=True)


def _create_or_update_env_var_dotpy(c, site_name):
    create_or_update_expr = 'grep -qxF "{0}" env_var.py || echo "{0}" >> env_var.py'

    create_or_update_header = create_or_update_expr.format('import os')
    c.run(create_or_update_header)

    create_or_update_debug = create_or_update_expr.format('os.environ[\'DJANGO_DEBUG_FALSE\'] = \'y\'')
    c.run(create_or_update_debug)

    create_or_update_sitename = create_or_update_expr.format(f'os.environ[\'SITENAME\'] = \'{site_name}\'')
    c.run(create_or_update_sitename)

    current_contents = c.run('cat env_var.py').stdout
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        c.run(f'echo "os.environ[\'DJANGO_SECRET_KEY\'] = \'{new_secret}\'" >> env_var.py')


def _create_or_update_dotenv(c, site_name):
    create_or_update_expr = 'grep -qxF "{0}" .env || echo "{0}" >> .env'

    create_or_update_debug = create_or_update_expr.format('export DJANGO_DEBUG_FALSE=y')
    c.run(create_or_update_debug)

    create_or_update_sitename = create_or_update_expr.format(f'export SITENAME={site_name}')
    c.run(create_or_update_sitename)

    password = os.environ['RECIPIENT_EMAIL_PASSWORD']
    create_or_update_test_pw = create_or_update_expr.format(f'export RECIPIENT_EMAIL_PASSWORD={password}')
    c.run(create_or_update_test_pw)

    current_contents = c.run('cat .env').stdout
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        c.run(f'echo "export DJANGO_SECRET_KEY={new_secret}" >> .env')


def _update_static_files(c):
    c.run('~/venvs/tdd-django/bin/python manage.py collectstatic --noinput')


def _update_database(c):
    c.run('~/venvs/tdd-django/bin/python manage.py migrate --noinput')


def _copy_devil_passenger_config(c):
    c.run('cp deploy_tools/passenger_wsgi.py .')


def _update_passenger_config(c):
    c.run('cat passenger_wsgi.py | sed "s/PROJECT_NAME/superlists/g" | tee passenger_wsgi.py')


def _restart_devil_app(c, target_site):
    c.run(f'devil www restart {target_site}')
