# PyPhantom

PyPhantom is a web server providing a simple API to retrieve web pages via PhantomJS.

## Usage

`PhantomJS --ip=<IP to listen on> --port=<Port to listen on> --phantomjs=<Command to start PhantomJS>`

for example,

`PhantomJS --ip=127.0.0.1 --port=80 --phantomjs=phantomjs.cmd`

## API

To retrieve a page via PhantomJS:-

`http://ListenIP:Port/get?url=http://example.com&screenshot=false`

* Listen IP and Port are as specified in command line
* URL is any valid URL
* Screenshot is a boolean value (true or false) of whether to save a screenshot of the page or not. The screenshot will have a random 16 character name with the png extension and will be returned along with the page HTML.

This request will return something similar to:-

`{
"result": "<!DOCTYPE html> [...] </html>",
"screenshot": "Y5WG3JgKeoOt6ZSH.png"
}`

However, the screenshot field will be omitted if not requested.

## Key Information

* PyPhantom waits 10 seconds for the page to load before capturing and returning the source, this should be enough time for the page JS to load all content.
* Untested in production
* Untested on OSX/Linux