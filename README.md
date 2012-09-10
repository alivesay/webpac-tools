webpac-tools
============

A collection of CLI and RESTful interfaces to Millennium WebPAC.


CLI: webpac
------------------------------

This tools provides a command line interface to WebPAC functions.

You must specify the Millennium server, either through the `--server` parameter, or by setting the environment variable `WEBPAC_SERVER`.

Other environment variables supported:
* `WEBPAC_PORT` -- sets the web server port for the WebPAC server (default: 443)

### $ webpac
```
$ webpac --help

usage: webpac [-h] [--server SERVER] [--port PORT] [--no_ssl] [--debug]
              {change_pin,modify_contact_info,register,get_contact_info} ...

Provides a CLI wrapper to Millennium WebPAC functions.

positional arguments:
  {change_pin,modify_contact_info,register,get_contact_info}
                        sub-command help
    change_pin          change patron's PIN
    modify_contact_info
                        modify patron's contact information
    register            register a new patron
    get_contact_info    get patron's current contact information

optional arguments:
  -h, --help            show this help message and exit
  --server SERVER       hostname or IP of Millennium server
  --port PORT           remote WebPAC port on the Millennium server (default:
                        443)
  --no_ssl              disable server connection
  --debug               enable diagnostic output
```

### $ webpac change_pin
```
$ webpac change_pin --help

usage: webpac change_pin [-h] BARCODE PIN NEW_PIN

positional arguments:
  BARCODE     patron's barcode
  PIN         patron's PIN
  NEW_PIN     new PIN

optional arguments:
  -h, --help  show this help message and exit
```

### $ webpac modify_contact_info
```
$ webpac modify_contact_info --help

usage: webpac modify_contact_info [-h]
                                  BARCODE PIN ADDRESS_LINE_1 ADDRESS_LINE_2
                                  TELEPHONE EMAIL LOCATION_CODE

positional arguments:
  BARCODE         patron's barcode
  PIN             patron's PIN
  ADDRESS_LINE_1  address line one
  ADDRESS_LINE_2  address line two
  TELEPHONE       telephone number
  EMAIL           email address
  LOCATION_CODE   default branch location code

optional arguments:
  -h, --help      show this help message and exit
```

### $ webpac get_contact_info
```
usage: webpac get_contact_info [-h] BARCODE PIN

positional arguments:
  BARCODE     patron's barcode
  PIN         patron's PIN

optional arguments:
  -h, --help  show this help message and exit
```

### $ webpac register
```
$ webpac register --help

usage: webpac register [-h]
                       FIRST_NAME MIDDLE_NAME LAST_NAME MAILING_ADDRESS_LINE_1
                       MAILING_ADDRESS_LINE_2 STREET_ADDRESS_LINE_1
                       STREET_ADDRESS_LINE_2 TELEPHONE EMAIL BIRTHDATE

positional arguments:
  FIRST_NAME            first name
  MIDDLE_NAME           middle name
  LAST_NAME             last name
  MAILING_ADDRESS_LINE_1
                        mailing address line 1
  MAILING_ADDRESS_LINE_2
                        mailing address line 2
  STREET_ADDRESS_LINE_1
                        street address line 1
  STREET_ADDRESS_LINE_2
                        street address line 2
  TELEPHONE             telephone (XXX-XXX-XXXX)
  EMAIL                 email address
  BIRTHDATE             birthdate (MMDDYYYY)

optional arguments:
  -h, --help            show this help message and exit
```

RESTful Web Service: app.py
---------------------------

This [bottle](http://bottlepy.org)-based module presents a web service interface to `WebPACSession`.  

Edit `app.py` and set `CATALOG_URL` to the URL of your WebPAC server.

* /change_pin, method: PUT, params: none, body:

```
'{"code":"1234567890000", "pin":"1234", "new_pin":"5678"}'
```

* /modify_contact_info, method: PUT, params: none, body:

```
'{"code":"1234567890000", "pin":"1234",
  "address_line_1":"1 Main Street", "address_line_2":"Apt. A",
  "email":"foo@bar.com, "location_code":"aa", "telephone":"000-867-5309" }'
```

* /register, method: PUT, params: none, body:

```
'{"first_name":"John", "middle_name":"A", "last_name":"Smith",
  "mailing_address_line_1":"1 Main Street",
  "mailing_address_line_2":"Washington DC 12345",
  "street_address_line_1":"2 Main Street",
  "street_address_line_2":"Washington DC 12345",
  "telephone":"123-456-7890", "email":"foo@bar.com", "birthdate":"19780814"}
```

* /contact_info, method: GET, params: (code, pin), body: none

WebPACSession.py
----------------

This module provides the core functionality for interfacing with WebPAC using web scraping techniques (thanks to the awesome BeautifulSoup library).

```
CLASSES
    WebPACSession

    class WebPACSession
     |  Provides access to WebPAC functions, maintaining web
     |  sessions where required.
     |
     |  Methods defined here:
     |
     |  __init__(self, url, debug=False)
     |
     |  change_pin(self, pin, new_pin)
     |      Changes a patron's PIN.
     |
     |  get_contact_info(self)
     |      Gets the patron's current contact information.
     |
     |  login(self, code, pin)
     |      Logs into a WebPAC session.
     |
     |  modify_contact_info(self, address_line_1, address_line_2,
     |                      telephone, email, location_code)
     |      Sets patron's contact information.
     |
     |  new_session(self)
     |      Gets a fresh WebPAC session cookie.
     |
     |  register(self, first_name, middle_name, last_name, mailing_address_line_1,
     |           mailing_address_line_2, street_address_line_1,
     |           street_address_line_2, telephone, email, birthdate)
     |      Registers a new patron.
     |
     |  request(self, resource, params=None)
     |      Manages web request to WebPAC server.
```
