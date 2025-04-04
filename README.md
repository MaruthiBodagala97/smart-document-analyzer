# Smart Document Analyzer

An AI-powered document analysis tool that extracts key information, summarizes content, and provides insights from various document formats.

## Features

- Document upload and processing (PDF, DOCX, TXT)
- AI-powered content analysis and summarization
- Key information extraction
- Sentiment analysis
- Topic modeling
- RESTful API with authentication
- Modern React frontend

## Tech Stack

- **Backend:** FastAPI, Python
- **Frontend:** React, TypeScript
- **AI/ML:** LangChain, OpenAI
- **Authentication:** JWT
- **Testing:** pytest
- **Documentation:** OpenAPI/Swagger

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-document-analyzer.git
cd smart-document-analyzer
```

2. Install backend dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```


4. Start the backend server:
```bash
uvicorn app.main:app --reload
```

5. Start the frontend development server:
```bash
cd frontend
npm start
```



## Testing

Run the tests with:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

