# Human-Guided Meteorology Agent

A clean, well-structured Python project that implements a Gemini-powered agent for weather information retrieval with human-in-the-loop capabilities.

## Features

- **Gemini Integration**: Uses Google's Gemini API for natural language processing
- **Web Search**: Integrates with Tavily for real-time weather information
- **Human Interaction**: Supports human-in-the-loop workflows
- **Clean Architecture**: Well-organized codebase with separation of concerns
- **Configuration Management**: Environment-based configuration
- **Testing**: Unit tests included

## Project Structure

```
human-guided-meteorology/
├── src/
│   ├── agent/
│   │   ├── core.py          # Main agent logic
│   │   ├── tools.py         # Search and ask_human tools
│   │   └── workflow.py      # State machine and workflow
│   ├── config/
│   │   └── settings.py      # Configuration management
│   └── utils/               # Utility modules
├── tests/                   # Unit tests
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── main.py                # Entry point
└── README.md              # This file
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd human-guided-meteorology
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

## Configuration

Create a `.env` file with your Google Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### Running the Agent

```bash
python main.py
```

### Programmatic Usage

```python
from src.agent.workflow import AgentWorkflow

# Create workflow
workflow = AgentWorkflow()

# Invoke with a query
response = workflow.invoke("Ask the user where they are, then look up the weather there")

# Resume with human response
response = workflow.resume("San Francisco, California")
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Development

### Code Style

The project follows PEP 8 standards. Use the following tools for code formatting:

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

### Adding New Features

1. Follow the existing architecture patterns
2. Add appropriate type hints
3. Write unit tests for new functionality
4. Update documentation as needed

## Dependencies

### Core Dependencies
- `google-generativeai`: Google Gemini API client
- `langchain`: LLM framework and tools
- `langgraph`: State machine and workflow management
- `langchain-tavily`: Web search integration

### Development Dependencies
- `pytest`: Testing framework
- `black`: Code formatter
- `flake8`: Linting
- `mypy`: Type checking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the test cases for usage examples# human-guided-metrology
