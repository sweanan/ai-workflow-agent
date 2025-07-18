#!/bin/bash

# Python AI Workflow Agent Docker Container Entrypoint Script
# This script runs the Python AI Workflow Agent inside the Docker container

set -e

echo "::group::Python AI Workflow Agent - Starting Docker Container"
echo "Python AI Workflow Agent starting..."

# Set verbose mode if requested
if [ "$INPUT_VERBOSE" == "true" ]; then
  set -x
  echo "Verbose mode enabled"
fi

echo "Operation: $INPUT_OPERATION"
echo "Target: $INPUT_TARGET"
echo "Verbose: $INPUT_VERBOSE"

# Run the Python application
echo "Running Python AI Workflow Agent..."
python src/main.py

# Check if the output file was created
if [ -f "/tmp/github_output.txt" ]; then
  echo "Agent completed successfully, setting outputs..."
  
  # Read the outputs from the file
  while IFS= read -r line; do
    echo "$line" >> $GITHUB_OUTPUT
  done < "/tmp/github_output.txt"
  
  echo "Outputs set successfully"
else
  echo "Warning: No output file found, setting default success outputs"
  echo "result=Python AI Workflow Agent completed" >> $GITHUB_OUTPUT
  echo "status=success" >> $GITHUB_OUTPUT
fi

echo "Python AI Workflow Agent container execution completed"
echo "::endgroup::"
