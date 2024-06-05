<div align="center">
  <img height="300" width="300" src="https://github.com/pablos123/dptn/assets/52180403/4ebe77fd-32b3-4676-aa60-4b4b25352353"/>
</div>

# Debian Package Tracker News

Fetch and search news from Debian Package Tracker. (https://tracker.debian.org)

## Install

`pip install git+https://github.com/pablos123/dptn.git`

## Examples

Fetch the news for _nginx_ package.

```
dptn -f openssl nginx
```

Search "deb10" string for _openssl_ package.

```
dptn -s deb10 openssl
```

Search "deb10" **and** "2019" strings for _openssl_ **and** _deb10_ packages.

```
dptn -s deb10 -s 2019 nginx openssl
```

Fetch packages before search.

```
dptn -f -s deb10 -s 2019 nginx openssl
```

Print all news for _openssl_ package but do it without escaped sequences.

```
dptn --no-color openssl
```

Help.

```
dptn -h
```

## More complex stuff

If you want to do another kind of operation you can work with the news files directly. The files are located in `~/.dptn/` after fetching the news.

There are two files per package:

- `<package_name>`
- `<package_name>.json`

Each line in the first file is a news for the package and each news is in the form:
`<date>;;<title>;;url`

The `.json` file is a list of hashes, each hash is a news.

### Examples

`or` operation using `rg`

```
echo && rg --color always --smart-case --no-line-number '2003-10|1.1.1' openssl | sed -z '$ s/\n/\n\n/g' | sed 's/;;/\n/g'
```

Pipe to `jq` then do whatever

```
cat nginx.json | jq ...
```
