#!/bin/sh

gunicorn wsgi:app --reload