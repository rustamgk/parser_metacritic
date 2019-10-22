# Metacritic parser update

virtualenv -p python3 --no-site-packages venv
source venv/bin/activate
pip install -r requirements-dev.txt

the followingf command will be registered and Its the way to run:
metacriticapp  [-h] or [--help] [-p] or [--platform]  [-a] or [--available] [-s] or [--search] [-f] or [--filename] [-r] or [--restapi] [-i] or [--ip] [-t] or [--port]
 
 or 

python3 -m metacritic [-h] or [--help] [-p] or [--platform]  [-a] or [--available] [-s] or [--search] [-f] or [--filename] [-r] or [--restapi] [-i] or [--ip] [-t] or [--port]

to run the tests:
python3 -m unittest