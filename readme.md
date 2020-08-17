# Dq Dev

<!--- mdtoc: toc begin -->

1.	[Synopsis](#synopsis)
2.	[Configuration](#configuration)
3.	[Dependencies](#dependencies)<!--- mdtoc: toc end -->

## Synopsis

My personal daiquiri dev setup which tries to keep things simple. Shell tools are mounted in volumes. Make sure to check the volume settings in `conf.yaml`. The following binaries are inside `shed` volume's folder. `Shed`s mountpoint is is the container's `$PATH`. Keep in mind that if you change the mountpoint `/vol/tools/shed` you need to change the `dockerfiles` as well.

folder and be available in path as they are used to run inside some of the containers.

1.	[caddy](https://github.com/caddyserver/caddy)
2.	[sd](https://github.com/chmln/sd)

Daiquiri is exposed on port `:9280`.

## Configuration

Configuration is basically done in `conf.yaml`. If you want your own local configuration feel free to use a copy of this file. Name it `conf_local.yaml`. The `conf_local.yaml` is read automatically if it exists. It is ignored by git and will avoid problems during pulling.

## Dependencies

A python script is used to render the `docker-compose.yaml`. The script is called by the makefile and requires `pyYAML`. Make sure it is installed. You can use the requirements file for that.

```
pip install -r requirements.txt
```
