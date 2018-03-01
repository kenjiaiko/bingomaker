# Debug
```
$ git clone https://github.com/kenjiaiko/bingomaker
$ cd bingomaker/server
$ chmod 705 setup.sh
$ ./setup.sh
$ chmod 705 reset.sh
$ ./reset.sh
```
It is necessary to set up [the server of challenge](https://github.com/kenjiaiko/bingomaker/tree/master/challenge) on localhost beforehand.
```
$ python checker.py localhost
$ cat result/localhost 
5.41382980347
```
The response speed of this server is 5.4138.
# Game
Each team have unique team ID (ex:1,2,3,4,....,15), it is tied to IP address. Players have to setup the service on 192.168.X.254. Admin server need to check all team's service on a regular basis.
## crontab -l
```
*/1 * * * * /usr/bin/python server/checker.py 192.168.1.254
*/1 * * * * /usr/bin/python server/checker.py 192.168.2.254
*/1 * * * * /usr/bin/python server/checker.py 192.168.3.254
...
*/1 * * * * /usr/bin/python server/checker.py 192.168.15.254
*/5 * * * * /usr/bin/python server/top_checker.py
```
checker.py will access to the service with the IP address, if there is a file with the "IP address name" under exec/. index.cgi make a file to in exec/.
