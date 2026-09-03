.PHONY: all build test run

all: build test

build:
	@echo "Building ai..."
	@npm run build

test:
	@echo "Running test suites for ai..."
	@npm test

run:
	@echo "Starting ai..."
	@node server.js
