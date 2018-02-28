# Debug
```
$ git clone https://github.com/kenjiaiko/bingomaker
$ cd bingomaker/server
$ chmod 705 setup.sh
$ ./setup.sh
$ chmod 705 reset.sh
$ ./reset.sh
```
It is necessary to set up [the server of challenge](https://github.com/kenjiaiko/bingomaker/tree/master/challenge) beforehand.
```
$ python checker.py localhost
$ cat result/localhost 
5.41382980347
```
The response speed of this server is 5.4138.
# Game
Each team have unique team ID (ex:1,2,3,4,....,15), it is tied to IP address. 
## crontab -l
```
*/1 * * * * /usr/bin/python server/checker.py 192.168.1.254
*/1 * * * * /usr/bin/python server/checker.py 192.168.2.254
*/1 * * * * /usr/bin/python server/checker.py 192.168.3.254
...
*/1 * * * * /usr/bin/python server/checker.py 192.168.15.254
*/4 * * * * /usr/bin/python server/top_checker.py
```
