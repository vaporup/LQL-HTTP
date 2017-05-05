# LQL-over-HTTP
Use [Check_MK livestatus LQL](https://mathias-kettner.de/checkmk_livestatus.html) over HTTP 

## Requirements

- [https://bottlepy.org](Bottle)
- [https://wsgi.readthedocs.io](WSGI)

## Installation

### WSGI and Bottle

```
apt-get install libapache2-mod-wsgi python-bottle
```

### Apache2 Config
Add the following lines to your VirtualHost

```
<VirtualHost *:80>

        WSGIScriptAlias   /lql /var/www/html/lql.wsgi
        WSGIDaemonProcess lql processes=2 threads=10
        WSGIProcessGroup  lql

</VirtualHost>
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
