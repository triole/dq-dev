# Dq Dev

<!--- mdtoc: toc begin -->

1.	[Synopsis](#synopsis)
2.	[How to use](#how-to-use)
3.	[Tech background](#tech-background)
	1.	[Dependencies](#dependencies)
	2.	[Tests](#tests)<!--- mdtoc: toc end -->

## Synopsis

My personal daiquiri dev setup. Shell tools are mounted by a volume called `shed` and reside in the equally named folder. The mountpoint of this folder is in $PATH.

## How to use

Interaction is done via the `manage.py` script. You can call `-h` for help.

A workflow could be

```python
# create a new profile
python manage.py -c newprof

# set it to active
python manage.py -s newprof

# and run it
python manage.py -r
```

Note that `-r` can also take a profile name as argument. But if none given the active profile will be used for the action. Same for other commands. The idea behind the `active profile` is that one does not have to pass the profile name as argument to the command one wants to run.

Profiles are saved in `usr/profiles/PROFILENAME`. Make sure you edit the `conf.yaml` there to adjust the settings you want to use.

## Tech background

I use [caddy](https://github.com/caddyserver/caddy) as http server and reverse proxy. Usually caddy is mounted into the daiquiri docker via the `shed` volume. If caddy does exist there, it will be used. If not the latest caddy will be pulled from github automatically.

### Dependencies

A python script is used to render the `docker-compose.yaml`. The script is called by the makefile and requires `pyYAML`. Make sure it is installed. You can use the requirements file for that.

```
pip install -r requirements.txt
```

### Tests

In the mainfolder is a python script `request_test.py` that fires some simple requests at Daiquiri. It helps to check proxy configurations. Try `python request_test.py -h` to find out what it can do.
