#!/bin/bash
if [ -z "$MODE" ] ; then
  MODE="PROD"
fi

if [ "$MODE" = "DEV" ] ; then
  uvicorn app:app --reload
elif [ "$MODE" = "PROD" ] ; then
  CPUNUMBER=`grep -c ^processor /proc/cpuinfo`
  WORKERS=`expr $CPUNUMBER \* 2`
  gunicorn app:app --workers $WORKERS --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
else
  uvicorn app:app --reload
fi