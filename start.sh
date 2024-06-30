#!/bin/bash

# Function to handle cleanup on exit
cleanup() {
  echo "Cleaning up..."
  kill $frontend_pid
  kill $backend_pid
  exit 0
}

# Trap the EXIT signal to run the cleanup function
trap cleanup EXIT

# Start the frontend (React)
cd frontend || exit
npm start &
frontend_pid=$!

export EVENTLET_HUB=poll

# Start the backend (Python Flask) with eventlet
cd ../backend || exit
python app.py &
backend_pid=$!

# Wait for both processes to complete
wait $frontend_pid
wait $backend_pid

