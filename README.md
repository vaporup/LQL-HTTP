# LQL-HTTP
Use [Check_MK livestatus LQL](https://mathias-kettner.de/checkmk_livestatus.html) over HTTP 

# Installation

## WSGI and Bottle

```
apt-get install libapache2-mod-wsgi python-bottle
```

## Apache2 Config

```
<VirtualHost *:80>

        WSGIScriptAlias   /lql /var/www/html/lql.wsgi
        WSGIDaemonProcess lql processes=2 threads=10
        WSGIProcessGroup  lql

</VirtualHost>
```
