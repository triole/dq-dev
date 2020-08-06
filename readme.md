# Dq Dev

<!--- mdtoc: toc begin -->

1.	[Synopsis](#synopsis)<!--- mdtoc: toc end -->

## Synopsis

My personal daiquiri dev setup which tries to keep things simple. Shell tools are mounted in volumes. Make sure to check the volume settings in `conf.yaml`. The following binaries are inside `shed` volume's folder. `Shed`s mountpoint is is the container's `$PATH`. Keep in mind that if you change the mountpoint `/vol/tools/shed` you need to change the `dockerfiles` as well.

folder and be available in path as they are used to run inside some of the containers.

1.	[caddy](https://github.com/caddyserver/caddy)
2.	[sd](https://github.com/chmln/sd)

Daiquiri is exposed on port `:9280`.
