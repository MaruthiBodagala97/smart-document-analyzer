from fastapi.testclient import TestClient
from app.main import app
import pytest
from pathlib import Path
import os

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Smart Document Analyzer API"}

def test_analyze_document_invalid_format():
    # Create a temporary file with invalid format
    with open("test.txt", "w") as f:
        f.write("This is a test document.")
    
    with open("test.txt", "rb") as f:
        response = client.post(
            "/analyze",
            files={"file": ("test.txt", f, "text/plain")}
        )
    
    # Clean up
    os.remove("test.txt")
    
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "key_points" in data
    assert "sentiment" in data
    assert "topics" in data

@pytest.mark.asyncio
async def test_analyze_document_error_handling():
    response = client.post(
        "/analyze",
        files={"file": ("test.xyz", b"invalid content", "application/octet-stream")}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"] 