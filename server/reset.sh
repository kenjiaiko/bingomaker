rm -rf db/*
for i in `seq 15`
do
python pysql.py
mv bingo.db db/192.168.$i.254.db
done
chmod 606 db/*
