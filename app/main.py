import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.src.pydantic_models import QueryInput, QueryResponse
 