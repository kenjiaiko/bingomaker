rm -rf db/*
rm -rf result/*
rm -rf exec/*
for i in `seq 15`
do
python pysql.py
mv bingo.db db/192.168.$i.254.db
done
python pysql.py
mv bingo.db db/localhost.db
chmod 606 db/*
