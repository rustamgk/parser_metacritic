Tutorial
=============

Requirements
------------
  - python v3.X
  - requests
  - BeautifulSoup
  - lxml


Installation
------------

  All the dependencies can be installed using PIP (Python Package Index)

  $ pip3 install beautifulsoup4 requests lxml 


  For additional information about the modules, please check the respective pages

  - `requests <http://docs.python-requests.org/en/master>`

  - `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup>`

  - 'lxml <https://lxml.de>'


Usage
------------

  **Name**


    metacritic.py - parse HTML for the “Top Games (By Metascore)” on Metacritic’s page (http://www.metacritic.com/)


  **Synopsis**


    metacritic.py [-h] or [--help] [-p] or [--platform]  [-a] or [--available] [-s] or [--search] [-f] or [--filename] [-r] or [--restapi] [-i] or [--ip] [-t] or [--port]


  **Description**


    This tutorial page documents the Python code metacritic.py, which is intended to parse the Metacritics score and returning a formated JSON output of the result.

    Another functionality is an exposed RESTAPI using Python  HTTPServer which allows a GET in /games/ to get all the scores and titles or a GET in /games/title_of_game.


Options
------------

  Options:
  -h, --help            show this help message and exit
  
  -p PLATFORM, --platform=PLATFORM
                        Platform to parse(ps4,xboxone,switch,pc,wii-u,3ds,vita,ios). default: ps4
						
  -a AVAILABLE, --available=AVAILABLE
                        Availability of games(new-releases, coming-soon, available). default: available
						
  -s SEARCH, --search=SEARCH
                        Key to form a request(To enter an argument with a space, you will have to enclose it in quotation marks "request with space"). default:None
						
  -f FILENAME, --filename=FILENAME
                        write output to FILE
						
  -r, --restapi         Use REST mode. defaul False
  
  -i HOST, --ip=HOST    IP for REST server. default: 0.0.0.0
  
  -t PORT, --port=PORT  Port for REST server. default: 8000

    **Examples:**

      PS4 all available games
        $ metacritic.py

      PS Vita coming-soon games 
        $ metacritic.py -p vita -a coming-soon

      Xbox One new-releases search Battlefield
        $ metacritic.py -p xboxone -a new-releases -s Battlefield

  RESTAPI   

    **Examples:**

      **PS4 all available games**

        $ parseMetacritics.py -r

      **Switch new-releases games**

        $ parseMetacritics.py -r -p switch -a new-releases
		
	For exposed RESTAPI browser GET in /games/ to get all the scores and titles or a GET in /games/title_of_game.
	
	**Examples:** 
	http://127.0.0.1:8000/games
	http://127.0.0.1:8000/games/Battlefield


Unit Tests
------------
  
  To execute tests:
  
  $ python3 -m unittest utest_metacritic
