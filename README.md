# bingomaker
* challenge/ - challenge files for players.
* checker/ - checking service program files for game admin.
## challenge
* put all files (challenge/) to /cgi-bin/
* make "pics/" dir to /var/www/html (the dir that another players can access on HTTP)
* write "pics/" dir path to status.json (in challenge/)
## checker
* write bingo.cgi path to status.json (in checker/)
* arg[1] of checker.py is IP address
* arg[2] of checker.py is value of num of the URL
