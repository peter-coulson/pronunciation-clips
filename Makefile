# Pronunciation Clips Testing Commands

# E2E Test Commands
test-e2e-all:
	pytest tests/e2e/ -v

test-e2e-stage1:
	pytest tests/e2e/test_stage1_foundation_e2e.py -v

test-e2e-stage2:
	pytest tests/e2e/test_stage2_audio_e2e.py -v

test-e2e-stage3:
	pytest tests/e2e/test_stage3_transcription_e2e.py -v

test-e2e-stage4:
	pytest tests/e2e/test_stage4_entities_e2e.py -v

test-e2e-stage5:
	pytest tests/e2e/test_stage5_database_e2e.py -v

test-e2e-stage6:
	pytest tests/e2e/test_stage6_pipeline_e2e.py -v

test-e2e-stage7:
	pytest tests/e2e/test_stage7_speakers_e2e.py -v

test-e2e-stage8:
	pytest tests/e2e/test_stage8_cli_e2e.py -v

# Unit test commands (will be created during implementation)
test-unit-all:
	pytest tests/unit/ -v

test-unit-stage1:
	pytest tests/unit/test_config.py tests/unit/test_models.py tests/unit/test_logging.py tests/unit/test_exceptions.py -v

# Integration test commands
test-integration-all:
	pytest tests/integration/ -v

# Full stage validation commands
test-stage1: test-unit-stage1 test-e2e-stage1
test-stage2: test-e2e-stage2
test-stage3: test-e2e-stage3
test-stage4: test-e2e-stage4
test-stage5: test-e2e-stage5
test-stage6: test-e2e-stage6
test-stage7: test-e2e-stage7
test-stage8: test-e2e-stage8

# Verification commands
verify-e2e-setup:
	pytest tests/e2e/ --collect-only

verify-all-tests:
	pytest tests/ --collect-only

# Cleanup commands
clean-test-output:
	rm -rf tests/output/*
	rm -rf temp/*

clean-all:
	rm -rf tests/output/*
	rm -rf temp/*
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Development helpers
install-deps:
	pip install -r requirements.txt
	pip install pytest

setup-dev:
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	source venv/bin/activate && pip install pytest click pydantic structlog

# Demo commands (will be created during implementation)
demo-stage1:
	python demos/demo_foundation.py

demo-stage2:
	python demos/demo_audio.py

demo-stage3:
	python demos/demo_transcription.py

demo-stage4:
	python demos/demo_entities.py

demo-stage5:
	python demos/demo_database.py

demo-stage6:
	python demos/demo_pipeline.py

demo-stage7:
	python demos/demo_speakers.py

# Help
help:
	@echo "Available commands:"
	@echo "  test-e2e-all        - Run all E2E tests"
	@echo "  test-e2e-stageN     - Run specific stage E2E test"
	@echo "  test-unit-all       - Run all unit tests"
	@echo "  test-integration-all - Run all integration tests"
	@echo "  test-stageN         - Run all tests for specific stage"
	@echo "  verify-e2e-setup    - Verify E2E tests are discoverable"
	@echo "  clean-test-output   - Clean test output directories"
	@echo "  install-deps        - Install project dependencies"
	@echo "  setup-dev           - Setup development environment"

.PHONY: test-e2e-all test-e2e-stage1 test-e2e-stage2 test-e2e-stage3 test-e2e-stage4 test-e2e-stage5 test-e2e-stage6 test-e2e-stage7 test-e2e-stage8 test-unit-all test-integration-all verify-e2e-setup clean-test-output clean-all install-deps setup-dev help