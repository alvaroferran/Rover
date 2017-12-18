
#!/bin/sh

route="/home/nanopi/mjpg-streamer/mjpg-streamer/"
cd  $route
./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -n -f 7 -r QVGA" -o "./output_http.so -w ./www"

exit 0


