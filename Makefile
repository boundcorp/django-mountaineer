#
# Main Makefile for project development and CI
#

# Default shell
SHELL := /bin/bash
# Fail on first error
.SHELLFLAGS := -ec

# Global variables
LIB_DIR := ./
LIB_NAME := django_mountaineer

EXAMPLE_DIR := ./example
EXAMPLE_NAME := .

SCRIPTS_DIR := .github
SCRIPTS_NAME := scripts

# Ignore these directories in the local filesystem if they exist
.PHONY: lint test

# Main lint target
lint: lint-lib lint-scripts

# Lint validation target
lint-validation: lint-validation-lib lint-validation-example

# Testing target
test: test-lib test-example

# Integration testing target
test-integrations: test-lib-integrations test-example-integrations

# Install all sub-project dependencies with poetry
install-deps: install-deps-lib install-deps-example

install-deps-lib:
	@echo "Installing dependencies for $(LIB_DIR)..."
	@(cd $(LIB_DIR) && poetry install)

install-deps-example:
	@echo "Installing dependencies for $(EXAMPLE_DIR)..."
	@(cd $(EXAMPLE_DIR) && poetry install)

# Clean the current poetry.lock files, useful for remote CI machines
# where we're running on a different base architecture than when
# developing locally
clean-poetry-lock:
	@echo "Cleaning poetry.lock files..."
	@rm -f $(LIB_DIR)/poetry.lock
	@rm -f $(EXAMPLE_DIR)/poetry.lock

# Standard linting - local development, with fixing enabled
lint-lib:
	$(call lint-common,$(LIB_DIR),$(LIB_NAME))
lint-example:
	$(call lint-common,$(EXAMPLE_DIR),$(EXAMPLE_NAME))

# Lint validation - CI to fail on any errors
lint-validation-lib:
	$(call lint-validation-common,$(LIB_DIR),$(LIB_NAME))
lint-validation-example:
	$(call lint-validation-common,$(EXAMPLE_DIR),$(EXAMPLE_NAME))

# Tests
test-lib:
	(cd $(LIB_DIR) && docker compose -f example/docker-compose.test.yml up -d)
	@$(call wait-for-postgres,30,5438)
	@set -e; \
	$(call test-common,$(LIB_DIR),$(LIB_NAME))
	(cd $(LIB_DIR) && docker compose -f example/docker-compose.test.yml down)
test-lib-integrations:
	$(call test-common-integrations,$(LIB_DIR),$(LIB_NAME))
test-example:
	$(call test-common,$(EXAMPLE_DIR),$(EXAMPLE_NAME))
test-example-integrations:
	$(call test-common-integrations,$(EXAMPLE_DIR),$(EXAMPLE_NAME))
test-scripts:
	$(call test-common,$(SCRIPTS_DIR),$(SCRIPTS_NAME))

#
# Common helper functions
#

define test-common
	echo "Running tests for $(2)..."
	@(cd $(1) && poetry run pytest -vvv -W error $(test-args) $(2))
endef

# Use `-n auto` to run tests in parallel
define test-common-integrations
	echo "Running tests for $(2)..."
	@(cd $(1) && poetry run pytest -s -m integration_tests -W error $(2))
endef

define lint-common
	echo "Running linting for $(2)..."
	@(cd $(1) && poetry run ruff format $(2))
	@(cd $(1) && poetry run ruff check --fix $(2))
	echo "Running mypy for $(2)..."
	@(cd $(1) && poetry run mypy $(2))
	echo "Running pyright for $(2)..."
	@(cd $(1) && poetry run pyright $(2))
endef

define lint-validation-common
	echo "Running lint validation for $(2)..."
	@(cd $(1) && poetry run ruff format --check $(2))
	@(cd $(1) && poetry run ruff check $(2))
	echo "Running mypy for $(2)..."
	@(cd $(1) && poetry run mypy $(2))
	echo "Running pyright for $(2)..."
	@(cd $(1) && poetry run pyright $(2))
endef

# Function to wait for PostgreSQL to be ready
define wait-for-postgres
	@echo "Waiting for PostgreSQL to be ready..."
	@timeout=$(1); \
	while ! nc -z localhost $(2) >/dev/null 2>&1; do \
		timeout=$$((timeout-1)); \
		if [ $$timeout -le 0 ]; then \
			echo "Timed out waiting for PostgreSQL to start on port $(2)"; \
			exit 1; \
		fi; \
		echo "Waiting for PostgreSQL to start..."; \
		sleep 1; \
	done; \
	echo "PostgreSQL is ready on port $(2)."
endef
