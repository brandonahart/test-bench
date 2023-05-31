#!/usr/bin/env zsh

TOKEN=$(curl -s http://127.0.0.1:8000/timer/upload/ | egrep csrfmiddlewaretoken | sed -e 's/.*value="\([^"]*\).*/\1/')
echo "TOKEN=$TOKEN"

curl --cookie "csrftoken=$TOKEN" -H "X-CSRFToken: $TOKEN" http://127.0.0.1:8000/timer/upload/ -F title=cowboy -F file=@data/data.csv


