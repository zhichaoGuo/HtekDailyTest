from configparser import ConfigParser
import pytest

def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="choose env: test,beta,prod")
    parser.addini('env', help="choose env: test,beta,prod")


@pytest.fixture(scope='session')
def env_vars(request):
    cur_env = request.config.getoption('--env')
    print(cur_env)
    inifile = request.config.inifile
    conf = ConfigParser()
    conf.read(inifile)
    variables = {}
    if conf.has_section('global'):
        variables.update(conf.items('global'))
    if conf.has_section(cur_env):
        variables.update(conf.items(cur_env))
    return variables