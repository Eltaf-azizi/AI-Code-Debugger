#!/bin/bash

# AI Code Assistant - Local Development Runner
# This script sets up and runs the application locally

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  AI Code Assistant - Local Runner${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating from example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}Please edit .env and add your OPENAI_API_KEY${NC}"
    else
        echo -e "${RED}Error: .env.example not found${NC}"
        exit 1
    fi
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}Python version: $PYTHON_VERSION${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Run database migrations
echo -e "${YELLOW}Setting up database...${NC}"
python scripts/seed_db.py

# Start the API server
echo -e "${GREEN}Starting API server...${NC}"
echo -e "${GREEN}API will be available at: http://localhost:8000${NC}"
echo -e "${GREEN}API docs at: http://localhost:8000/docs${NC}"

# Run the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
