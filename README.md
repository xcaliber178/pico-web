# pico-web

## Pico W webserver playground

This project is a learning experiment for myself to learn about Python (MicroPython), web design languages, low level IP/ICP stacks, and other related network functions. This is also my first GitHub experiance so I'm learning about proper programming conventions and project documentation.

I'm sure that most of what is in this project can be could in various forms across the internet, but maybe someone will find something new here. Feel free to do with it what you please and offer any comments you care to.

## The Program
The main goal of the program is to serve a webpage to local and remote web browser clients. The webpage contains information generated from the Pico W which is passed into the HTML file. It also has an external CSS file to handle the page stying, this CSS file is also served from the Pico W. 

The general flow can be see in `main.py`. _Connect to wifi -> Sync RTC to NTP -> Begin serving webpage_
Note that this is a fully synchronous program. A rewrite with `asyncio` is planned.
Also note that this is written for a Raspberry Pi Pico W with **no regard for compatibility with other devices**.

### [pico.geisel.tech](http://pico.geisel.tech "See the page hosted from my Pico W")
