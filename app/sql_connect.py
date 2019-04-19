# pip
import psycopg2

def build_url(username='guest',
              password='guest',
              host='127.0.0.1',
              port=5432,
              database='sandbox',
              **kwargs) -> str:
    if isinstance(host, list) and isinstance(port, list):
        assert len(host) == len(port)
        addresses = ','.join([f'{h}:{p}' for h, p in list(zip(host, port))])
    else:
        addresses = f'{host}:{port}'

    if kwargs:
        query = '?' + '&'.join([f'{k}={v}' for k, v in kwargs.items()])
    else:
        query = ''

    url = f'postgresql://{username}:{password}@{addresses}/{database}{query}'
    print(f'Built PSQL url: {url}')
    return url


def create_url_from_config(config: dict) -> str:
    args = dict()
    args['username'] = config['psql']['username']
    args['password'] = config['psql']['password']
    args['host'] = config['psql']['host']
    args['port'] = config['psql']['port']
    args['database'] = config['psql']['database']

    kwargs = dict()
    if 'connection_parameters' in config['psql']:
        kwargs = config['psql']['connection_parameters']
    return build_url(**args, **kwargs)


def connect(url: str) -> psycopg2._psycopg.connection:
    connection = psycopg2.connect(url)
    assert not connection.closed, 'PSQL connection closed after connecting!'
    return connection


def connect_with_config(config: dict):
    url = create_url_from_config(config)
    print('Making connection')
    connection = connect(url)
    print('Connection made')
    return connection
