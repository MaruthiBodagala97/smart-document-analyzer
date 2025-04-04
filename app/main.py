from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Smart Document Analyzer",
    description="AI-powered document analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class DocumentAnalysis(BaseModel):
    summary: str
    key_points: list
    sentiment: str
    topics: list

# Helper functions
def get_document_loader(file: UploadFile):
    """Get the appropriate document loader based on file extension"""
    file_extension = file.filename.split('.')[-1].lower()
    
    # Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    try:
        if file_extension == 'pdf':
            return PyPDFLoader(temp_path)
        elif file_extension in ['docx', 'doc']:
            return Docx2txtLoader(temp_path)
        elif file_extension == 'txt':
            return TextLoader(temp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

def analyze_document(text: str) -> DocumentAnalysis:
    """Analyze document content using LangChain and OpenAI"""
    llm = OpenAI(temperature=0)
    
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    # Split text into chunks
    chunks = text_splitter.split_text(text)
    
    # Create analysis prompts
    summary_template = """
    Summarize the following text in a concise way:
    {text}
    """
    
    key_points_template = """
    Extract the key points from the following text:
    {text}
    """
    
    sentiment_template = """
    Analyze the sentiment of the following text (positive, negative, or neutral):
    {text}
    """
    
    topics_template = """
    Identify the main topics discussed in the following text:
    {text}
    """
    
    # Create chains
    summary_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=summary_template, input_variables=["text"])
    )
    
    key_points_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=key_points_template, input_variables=["text"])
    )
    
    sentiment_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=sentiment_template, input_variables=["text"])
    )
    
    topics_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=topics_template, input_variables=["text"])
    )
    
    # Run analysis
    summary = summary_chain.run(chunks[0])
    key_points = key_points_chain.run(chunks[0]).split('\n')
    sentiment = sentiment_chain.run(chunks[0])
    topics = topics_chain.run(chunks[0]).split('\n')
    
    return DocumentAnalysis(
        summary=summary,
        key_points=key_points,
        sentiment=sentiment,
        topics=topics
    )

# Routes
@app.post("/analyze", response_model=DocumentAnalysis)
async def analyze_document_endpoint(file: UploadFile = File(...)):
    """Analyze a document and return insights"""
    try:
        # Get document loader
        loader = get_document_loader(file)
        
        # Load and process document
        documents = loader.load()
        text = " ".join([doc.page_content for doc in documents])
        
        # Analyze document
        analysis = analyze_document(text)
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Smart Document Analyzer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 