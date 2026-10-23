.PHONY: all build install setup test test-go test-ref doctor clean help

SHELL := /bin/bash
BIN := bin/drills
PYTHON ?= .venv/bin/python3

all: build

build:
	@mkdir -p bin
	go build -o $(BIN) ./cmd/drills
	@echo "Built $(BIN)"

install: build
	@mkdir -p $(shell go env GOPATH)/bin
	cp $(BIN) $(shell go env GOPATH)/bin/drills
	@echo "Installed drills to $(shell go env GOPATH)/bin/drills"

setup:
	@if [ ! -d ".venv" ]; then \
		echo "Creating Python 3.14 virtual environment..."; \
		python3.14 -m venv .venv || /opt/homebrew/bin/python3.14 -m venv .venv; \
	fi
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pytest hypothesis pytest-timeout pyyaml
	@echo "Environment setup complete."

test: test-go test-ref

test-go:
	go test -v ./...

test-ref: build
	$(BIN) test --all --target reference

doctor: build
	$(BIN) doctor

clean:
	rm -rf bin/ .drills/active_session.json .pytest_cache/ __pycache__/

help:
	@echo "Algorithm Drills Build System"
	@echo "  make build       - Compile native Go drills binary"
	@echo "  make install     - Install drills to GOPATH/bin"
	@echo "  make setup       - Set up Python 3.14 virtualenv & dependencies"
	@echo "  make test-go     - Run Go framework unit tests"
	@echo "  make test-ref    - Run all 88 reference implementation tests"
	@echo "  make doctor      - Run drills doctor health checks"
	@echo "  make clean       - Clean build artifacts"
