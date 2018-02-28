# how to setup Web service
## bingo server
```
$ git clone https://github.com/kenjiaiko/bingomaker
$ cd bingomaker/challenge
$ chmod 705 setup.sh
$ ./setup.sh
$ chmod 705 exec.sh
$ ./exec.sh
Serving HTTP on 0.0.0.0 port 80 ...
```
Make sure that you can access to /cgi-bin/bingo.cgi and pics/ on HTTP
## check script for your server
```
$ cd bingomaker/challenge/checker/
$ python checker.py localhost
success
success
...
```
