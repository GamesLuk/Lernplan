#!/bin/bash

# Check if dependencies are already installed
if [ ! -f ".setup_done" ]; then
  echo "Installing repository dependencies..."
  git clone https://github.com/gamesluk/lernplan.git /app

  # Mark setup as done
  touch .setup_done
  echo "Setup completed."
else
  echo "Setup already completed. Skipping."
fi
