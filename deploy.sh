#!/bin/bash

# ==============================================================================
# Cognitive Entanglement - Automated Onboard Companion Deployment Script 🚀⚙️
# Language: Bash / Shell Scripting
# Target: Raspberry Pi / NVIDIA Jetson Nano / Radxa Zero (Phone A Alternative)
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}[DEPLOY]: Starting Cognitive Entanglement Board Deployment System...${NC}"

# Step 1: System Check & Update
echo -e "${BLUE}[DEPLOY]: Updating system package repositories...${NC}"
sudo apt-get update -y

# Step 2: Install core operating dependencies
echo -e "${BLUE}[DEPLOY]: Installing Python3, Pip, and development headers...${NC}"
sudo apt-get install -y python3-pip python3-dev python3-opencv build-essential libportaudio2

# Step 3: Install Python requirements
echo -e "${BLUE}[DEPLOY]: Installing Python framework requirements...${NC}"
pip3 install -r requirements.txt --upgrade

# Step 4: Compile Rust Safety-Critical Watchdog
if command -v rustc &> /dev/null; then
    echo -e "${BLUE}[DEPLOY]: Rust compiler found. Compiling High-Integrity Onboard Watchdog...${NC}"
    rustc -O src/failsafe_watchdog.rs --out-dir bin/
    echo -e "${GREEN}[SUCCESS]: Onboard Rust Watchdog binary compiled to bin/failsafe_watchdog.${NC}"
else
    echo -e "${RED}[WARNING]: Rust compiler (rustc) not found. Skipping Rust watchdog binary build.${NC}"
    echo -e "${BLUE}[INFO]: To compile, run: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh${NC}"
fi

echo -e "${GREEN}[SUCCESS]: Cognitive Entanglement Deployment Complete!${NC}"
echo -e "${BLUE}[INFO]: To launch the server, run: python3 src/dashboard.py${NC}"
