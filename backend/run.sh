#!/bin/sh

# PRODUCTION ONLY OTHERWISE THE BELOW LINE SHOULD BE A COMMENT
# . /backend/sandbox/bin/activate 

# RUN
gunicorn wsgi:app --reload