#!/bin/bash
gunicorn Backend:app --bind 0.0.0.0:$PORT
