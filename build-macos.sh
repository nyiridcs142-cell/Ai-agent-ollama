#!/bin/env bash
set -e

cd "$(dirname "$0")"

show_usage() {
  echo "Usage: ./build-macos.sh [run|build]"
}

check_python() {
  if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON=python
  else
    echo "Error: Python 3 was not found. Install it from python.org or with Homebrew."
    exit 1
  fi
}

setup_environment() {
  check_python
  if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    "$PYTHON" -m venv .venv
  fi
  source ".venv/bin/activate"
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
}

run_app() {
  setup_environment
  echo "Starting AI Agent..."
  python ai-agent.py
}

build_app() {
  setup_environment
  python -m pip install pyinstaller
  rm -rf dist/AI-Agent.app build/AI-Agent
  python -m PyInstaller ai-agent.spec --noconfirm --windowed --name "AI-Agent"
  if [ -d "dist/AI-Agent.app" ]; then
    echo "Build complete: dist/AI-Agent.app"
  else
    echo "Error: macOS app bundle could not be created."
    exit 1
  fi
}

case "${1:-run}" in
  run) run_app ;;
  build) build_app ;;
  -h|--help) show_usage ;;
  *) show_usage; exit 1 ;;
esac
