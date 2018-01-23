# bingomaker
bingomaker is one of the hacking game to speed up Web service. 
* challenge/* - challenge files for players.
* checker/* - checking service program files for game admin.
## challenge
* put all files (challenge/*) to /cgi-bin/
* make "pics/" dir to /var/www/html/ (the dir that another players can access on HTTP)
* write "pics/" dir path to status.json (in challenge/)
* make sure that you can access to /cgi-bin/challenge/bingo.cgi and pics/ on HTTP
## checker
* write bingo.cgi path to status.json (in checker/)
* arg[1] of checker.py is IP address
* arg[2] of checker.py is the num of bingo images you want to create
* printed value executing checker.py, is a response time of the service
