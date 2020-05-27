# Dq Dev

<!--- mdtoc: toc begin -->

1.	[Synopsis](#synopsis)
2.	[Local Tests](#local-tests)
	1.	[Add Test Data](#add-test-data)
	2.	[Migrate](#migrate)
3.	[Query Examples](#query-examples)
	1.	[Synchronous Request](#synchronous-request)
4.	[Docs](#docs)
5.	[URLs](#urls)<!--- mdtoc: toc end -->

## Synopsis

My personal daiquiri dev setup which tries to keep things simple. Shell tools are mounted in volumes. Make sure to check the volume settings in `dc_master.yaml`. The following binaries are required and need to be available in path.

1.	[caddy](https://github.com/caddyserver/caddy)
2.	[sd](https://github.com/chmln/sd)

Daiquiri is exposed on port `:9280`.

## Local Tests

### Add Test Data

```shell
# databases, users and permissions to run daiquiri
./manage.py sqlcreate                             

# databases, users and permissions to run tests
./manage.py sqlcreate --test                     

# databases, users and permissions to use a particular schema
./manage.py sqlcreate --schema=daiquiri_data_obs
```

### Migrate

```
./manage.py migrate
./manage.py migrate --database=data
```

## Query Examples

### Synchronous Request

```python
import requests
import pyvo as vo

auth = 'Token 51cccc3cdefbd4f6fe958b311f019460f53fde1d'
url = 'http://localhost:9494/tap'
query = 'SELECT TOP 5 source_id, ra, dec, parallax FROM gdr2.gaia_source ORDER BY random_index'

tap_session = requests.Session()
tap_session.headers['Authorization'] = auth
tap_service = vo.dal.TAPService(url)
tap_service.session = tap_session
tap_result = tap_service.run_sync(query)
tap_result.to_table()
print(tap_result)
```

## Docs

[Dev Setup](https://github.com/django-daiquiri/daiquiri/blob/master/docs/development.md)

## URLs

[http://localhost:9280](http://localhost:9280) [http://localhost:9280/cms](http://localhost:9280/cms)
