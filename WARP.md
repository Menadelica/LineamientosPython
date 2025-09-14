# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a **Python REFramework** implementation for automating prompt generation using Google Gemini API. It follows UiPath's REFramework pattern with five distinct phases: Initialization, Get Transaction, Process, Handle Errors, and End Process.

The system processes CSV input data containing prompts and generates detailed responses for UiPath automation scenarios using Gemini's AI capabilities.

## Essential Commands

### Environment Setup
```powershell
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies  
pip install -r requirements.txt

# Set API key (required)
$env:GEMINI_API_KEY="your_api_key_here"
```

### Core Operations
```powershell
# Run main automation process
python main.py

# Run direct Gemini example (for testing)
python gemini.py

# Show help and usage information
python main.py --help
```

### Testing
```powershell
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=framework tests/

# Run specific test class
pytest tests/test_process.py::TestGeminiProcessor

# Run specific test method
pytest tests/test_process.py::TestGeminiProcessor::test_processor_initialization
```

### Code Quality
```powershell
# Format code (if black is installed)
black .

# Lint code (if flake8 is installed)
flake8 framework/ tests/
```

## Architecture Overview

### REFramework Structure
The framework follows UiPath's proven REFramework pattern with these phases:

1. **Initialization** (`framework/init.py`): Loads config, sets up logging, verifies dependencies, loads input queue
2. **Get Transaction** (`framework/get_transaction.py`): Validates and prepares individual items for processing
3. **Process** (`framework/process.py`): Core business logic using Gemini API to generate responses
4. **Handle Error** (`framework/handle_error.py`): Classifies and handles BusinessException vs SystemException with retry logic
5. **End Process** (`framework/end.py`): Saves results, generates reports, cleans up resources

### Key Components

**GeminiProcessor Class** (`framework/process.py`):
- Manages Gemini API client lifecycle
- Structures prompts with context and expected output
- Processes streaming responses
- Classifies errors by type (business vs system)

**Error Classification System**:
- **BusinessException**: Data validation errors, invalid prompts (no retry)
- **SystemException**: API errors, network issues, authentication (retryable with exponential backoff)

**Configuration Management** (`config/settings.json`):
- Gemini model settings (model, thinking_budget, system_instruction)
- Logging configuration (level, format, file paths)
- Processing settings (max_retries, retry_delay, batch_size)
- File paths for input/output/logs

## Data Flow

### Input Format
CSV file at `data/input/prompts.csv` with columns:
- `id`: Unique identifier
- `prompt`: Main request text
- `context`: Optional context information
- `expected_output`: Optional description of desired result

### Output Files
- `data/output/results.csv`: Successful processing results
- `data/output/automation.log`: Main execution log
- `data/output/execution_report.json`: Final statistics and summary
- `data/output/business_errors.log`: Business rule violations
- `data/output/system_errors.log`: Infrastructure/API errors

## Development Guidelines

### Adding New Functionality
- Follow the existing REFramework phase structure
- Add corresponding tests in `tests/` directory
- Update configuration in `settings.json` if needed
- Maintain separation between business and system errors

### Error Handling Best Practices
- Classify errors correctly (business vs system) for appropriate retry behavior
- Use structured logging with appropriate levels (DEBUG, INFO, WARNING, ERROR)
- Always provide transaction ID context in error messages

### Testing Strategy
- Mock external API calls (Gemini) using `unittest.mock`
- Test both success and failure scenarios
- Verify error classification logic
- Test configuration loading and validation

### Configuration Changes
- Modify `config/settings.json` for system behavior
- Set `GEMINI_API_KEY` environment variable
- Create sample input files automatically if missing
- Use relative paths in configuration for portability

## Important Implementation Notes

### Gemini API Integration
- Uses streaming response processing for better user experience
- Implements thinking_budget configuration for response quality control
- Includes Google Search tools integration
- Structured system instructions for UiPath specialization

### Framework Modularity
Each framework module (`init.py`, `get_transaction.py`, `process.py`, `handle_error.py`, `end.py`) can be imported and used independently, following the single responsibility principle.

### Error Recovery
- System errors automatically retry up to `max_retries` times
- Business errors are logged but don't retry (fail-fast for data quality)
- All failures are tracked and included in final execution report

## File Structure Context

```
automation_project/
├── framework/           # REFramework implementation modules
├── config/settings.json # Central configuration
├── data/
│   ├── input/          # CSV input files (auto-created if missing)
│   └── output/         # Results, logs, and reports
├── tests/              # Comprehensive test suite
├── main.py            # Primary entry point
├── gemini.py          # Direct API example (for reference)
└── requirements.txt   # Python dependencies
```

The framework is designed to be robust, maintainable, and aligned with enterprise automation best practices from UiPath's REFramework pattern.
