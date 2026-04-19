# 1. shell into namenode
docker exec -it ndx00 bash

# 2. list the images directory
hdfs dfs -ls /ksvx/images

# 3. count total files
hdfs dfs -count /ksvx/images

# 4. check disk usage
hdfs dfs -du -h /ksvx/images

# list root
hdfs dfs -ls /

# list ksvx directory
hdfs dfs -ls /ksvx

# list images directory
hdfs dfs -ls /ksvx/images

# count files in images directory
hdfs dfs -count /ksvx/images

# disk usage of images directory (human readable)
hdfs dfs -du -h /ksvx/images

# disk usage summary of images directory
hdfs dfs -du -s -h /ksvx/images

# total disk usage of entire ksvx directory
hdfs dfs -du -s -h /ksvx

# check overall capacity and usage
hdfs dfsadmin -report

# check namenode status
hdfs dfsadmin -safemode get
