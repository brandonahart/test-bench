#!/bin/zsh

CSRFTOKEN=$1

echo "Starting: " 

curl --cookie "csrftoken=$CSRFTOKEN" -H "X-CSRFToken: $CSRFTOKEN" http://127.0.0.1:8000/timer/upload/ -F title=cowboy -F file=@../data/data.csv -F choice="DIRECTORY" &&

curl --cookie "csrftoken=$CSRFTOKEN" -H "X-CSRFToken: $CSRFTOKEN" http://127.0.0.1:8000/timer/upload/ -F title=cowboy -F file=@../data/data.csv -F choice="SQLITE" &&

curl --cookie "csrftoken=$CSRFTOKEN" -H "X-CSRFToken: $CSRFTOKEN" http://127.0.0.1:8000/timer/upload/ -F title=cowboy -F file=@../data/data.csv -F choice="MONGO" &&

#curl http://127.0.0.1:8000/timer/brandon/0/ &
#curl http://127.0.0.1:8000/timer/joe/0/ &
#curl http://127.0.0.1:8000/timer/tim/0/ &
#curl http://127.0.0.1:8000/timer/luke/0/ &
#curl http://127.0.0.1:8000/timer/max/0/ &
#curl http://127.0.0.1:8000/timer/logan/0/ &
#curl http://127.0.0.1:8000/timer/cole/0/ &

echo "Finish: " 
