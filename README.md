# Digital-KYC
This project includes a secure and intelligent digital KYC (Know Your Customer) system that leverages Al-powered document analysis and facial recognition to verify user identities
A Secure, Automated Solution for Document Verification and Facial Recognition

# Overview

This project implements an AI-powered Digital KYC (Know Your Customer) and Identity Verification System that:
 Detects forged/tampered documents (Aadhaar, Passport, PAN, Driver’s License)
 Performs facial recognition to match ID photos with live selfies
 Ensures GDPR & DPDP Act compliance with secure data handling
 Provides a modular, scalable API for integration into banking, fintech, and eKYC platforms

Built with Python, OpenCV, Dlib, and Deep Learning models for high accuracy.

# Features

1. Document Verification
OCR-based text extraction (Tesseract, EasyOCR)
Fraud detection (ML-based tampering detection)
MRZ & Barcode parsing for passports and IDs

3. Facial Recognition
Face detection & alignment (Dlib, MTCNN)
Face matching (FaceNet, DeepFace)
Liveness detection (anti-spoofing)

4. Security & Compliance
Data encryption (AES-256)
GDPR & DPDP-compliant storage
Automated redaction of sensitive data (PII protection)


Run the folowing command in your terminal or CLI to install required libraries
1. For document verification
pip install tensorflow==2.12.0 numpy==1.23.5 protobuf==3.20.3 streamlit==1.30.0 easyocr==1.7.0 opencv-python-headless==4.9.0.80 Pillow==10.2.0 deepface==0.0.79

2. For live image capture
pip install face_recognition pip install dlib face_recognition pip install opencv-python   
