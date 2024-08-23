# Resume-Screening-and-Ranking-System
## Overview
This project is a Resume Screening and Ranking System designed to help recruiters and HR professionals efficiently evaluate and rank resumes based on their relevance to a given job description. The system uses Natural Language Processing (NLP) techniques to match the content of resumes against the job description and ranks them accordingly.
## Features
Multi-format Resume Upload: Supports PDF, DOCX, and TXT formats.

Text Extraction: Extracts text from resumes using docx2txt and PyPDF2 for DOCX and PDF files, respectively.

NLP-based Matching: Utilizes TF-IDF vectorization and cosine similarity to evaluate how well each resume matches the job description.

Ranking System: Displays resumes ranked in order of their relevance to the job description.

Flask-based Web Interface: User-friendly interface for uploading resumes and viewing the results.
## Technologies Used
Flask: For the web interface and application server.

NLP Libraries: Scikit-learn for TF-IDF vectorization and cosine similarity.

Text Extraction: docx2txt for DOCX files and PyPDF2 for PDF files.

HTML/CSS: For the frontend design with Bootstrap for responsive design.
