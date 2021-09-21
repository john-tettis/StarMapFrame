#!/bin/sh

# PRODUCTION ONLY OTHERWISE THE BELOW LINE SHOULD BE A COMMENT
# . /backend/sandbox/bin/activate 

# RUN
gunicorn wsgi:app --reload --timeout 600 --workers=3 --threads=3 --worker-connections=1000