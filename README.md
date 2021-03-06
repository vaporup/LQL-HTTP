# LQL-over-HTTP(s)
Use [Check_MK livestatus LQL](https://mathias-kettner.de/checkmk_livestatus.html) over HTTP(s).

Inspired by [Livestatus-Rest-Interface
](https://github.com/py-man/Livestatus-Rest-Interface) and [rest-mk-livestatus
](https://github.com/giuliano108/rest-mk-livestatus)

## Requirements

- [Bottle](https://bottlepy.org)
- [WSGI](https://wsgi.readthedocs.io)

## Installation (Debian-based Distros)

### WSGI and Bottle

```
apt-get install libapache2-mod-wsgi python-bottle
```

## Config

### Apache2
Add the following lines to your VirtualHost section

```
WSGIScriptAlias   /lql /var/www/html/lql.wsgi
WSGIDaemonProcess lql processes=2 threads=10
WSGIProcessGroup  lql
```

### Livestatus Host and Port

If needed, change Livestatus host and port in **lql.wsgi**

#### Default

```python
LIVESTATUS_HOST = '127.0.0.1'
LIVESTATUS_PORT = 6557
```

## Usage

### query.lql

```
GET hosts
Columns: name
Limit: 2
```

### post query

```
curl -X POST --data-binary @query.lql http://127.0.0.1/lql/

```
