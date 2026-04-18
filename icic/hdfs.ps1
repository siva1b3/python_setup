
# 1. shell into namenode
docker exec -it etl-namenode bash

# 2. list the images directory in HDFS
hdfs dfs -ls /etl/images

# 3. count total files
hdfs dfs -count /etl/images

# 4. check disk usage
hdfs dfs -du -h /etl/images

# list root
hdfs dfs -ls /

# list etl directory
hdfs dfs -ls /etl

# list images directory
hdfs dfs -ls /etl/images

# count files in images directory
hdfs dfs -count /etl/images

# disk usage of images directory (human readable)
hdfs dfs -du -h /etl/images

# disk usage summary of images directory
hdfs dfs -du -s -h /etl/images

# total disk usage of entire etl directory
hdfs dfs -du -s -h /etl

# check HDFS overall capacity and usage
hdfs dfsadmin -report

# check namenode status
hdfs dfsadmin -safemode get