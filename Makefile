.PHONY: all build install setup test test-go test-ref doctor clean help

SHELL := /bin/bash
BIN := bin/drills
PYTHON ?= .venv/bin/python3
GOPATH_BIN := $(shell go env GOPATH)/bin
LOCAL_BIN := $(HOME)/.local/bin

all: install

build:
	@mkdir -p bin
	go build -o $(BIN) ./cmd/drills
	@echo "Built $(BIN)"

install: build
	@mkdir -p $(LOCAL_BIN)
	@cp -f $(BIN) $(LOCAL_BIN)/drills
	@chmod +x $(LOCAL_BIN)/drills
	@if [ -d "$(GOPATH_BIN)" ]; then \
		cp -f $(BIN) "$(GOPATH_BIN)/drills"; \
		chmod +x "$(GOPATH_BIN)/drills"; \
	fi
	@mkdir -p $(HOME)/.config/drills
	@echo "$(CURDIR)" > $(HOME)/.config/drills/root
	@echo "✔ Installed 'drills' to PATH: $(LOCAL_BIN)/drills and $(GOPATH_BIN)/drills"
	@echo "✔ Configured project directory for global execution from any directory."

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
	@echo "  make             - Compile and automatically install drills into your PATH"
	@echo "  make build       - Compile native Go binary to bin/drills"
	@echo "  make install     - Install drills to ~/.local/bin and GOPATH/bin"
	@echo "  make setup       - Set up Python 3.14 virtualenv & dependencies"
	@echo "  make test-go     - Run Go framework unit tests"
	@echo "  make test-ref    - Run all 88 reference implementation tests"
	@echo "  make doctor      - Run drills doctor health checks"
	@echo "  make clean       - Clean build artifacts"
