# Dq Dev

<!--- mdtoc: toc begin -->

1.	[Synopsis](#synopsis)
2.	[Configuration](#configuration)
3.	[Dependencies](#dependencies)<!--- mdtoc: toc end -->

## Synopsis

My personal daiquiri dev setup which tries to keep things simple. Shell tools are mounted by a volume called `shed` and reside in the equally named folder. The mountpoint of this folder is in $PATH. Make sure to check `conf.yaml` for volume settings. Please be aware that you need to adjust $PATH if you change mountpoints.

If your host is missing folders that are declared in `conf.yaml` the relevant volume will not be created and so not be available in your container. Note that daiquiri's and the app's source code are required. Make sure you have them on your host and that their folders are correctly configured in your `conf_local.yaml`.

I use [caddy](https://github.com/caddyserver/caddy) as http server and reverse proxy. Usually caddy is mounted into the daiquiri docker via the `shed` volume. If caddy does exist there, it will be used. If not the latest caddy will be pulled from github automatically.

Daiquiri is exposed on port `:9280`.

## Configuration

Configuration is basically done in `conf.yaml`. If you want your own local configuration feel free to use a copy of this file. Name it `conf_local.yaml`. The `conf_local.yaml` is read automatically if it exists. It is ignored by git and will avoid problems during pulling.

## Dependencies

A python script is used to render the `docker-compose.yaml`. The script is called by the makefile and requires `pyYAML`. Make sure it is installed. You can use the requirements file for that.

```
pip install -r requirements.txt
```
