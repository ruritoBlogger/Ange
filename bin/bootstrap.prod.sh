#!/bin/bash
source .env

uwsgi --http :$ANGE_PORT --wsgi-file index.py --callable app