# Adaptive Steganography-Based Secure Communication System

## Overview

A secure communication system that combines cryptography and adaptive image steganography to protect confidential information. The system analyzes message sensitivity, applies suitable security measures, and securely hides messages inside digital images.

## Project Structure

* `app.py` — User interface and application workflow
* `text_analysis.py` — Analyzes message content and detects sensitive information
* `classification.py` — Classifies messages based on sensitivity level
* `encryption.py` — Provides encryption mechanisms for protected messages
* `steganography.py` — Handles message embedding and extraction from images
* `requirements.txt` — Project dependencies

## Security Features

* Adaptive security based on message sensitivity level
* Cryptographic protection for restricted and confidential messages
* Image steganography for secure data hiding
* User authentication and security logging mechanisms

## Sensitivity Levels

* **Public:** Message is embedded without encryption
* **Restricted:** Message is encrypted before embedding
* **Confidential:** Message is encrypted and requires additional protection

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the application using:

```bash
streamlit run app.py
```

## Example Usage

1. Enter a message.
2. Upload an image.
3. The system analyzes and classifies the message sensitivity.
4. The message is encrypted if required.
5. The encrypted message is embedded into the image.
6. The generated stego-image can be saved securely.

For message extraction:

1. Upload the stego-image.
2. Enter the required password if applicable.
3. Extract and display the hidden message.

## Technologies Used

* Python
* Streamlit
* Cryptography
* Image Steganography
* Secure Data Handling

## Project Purpose

This project demonstrates how cryptography and steganography can be integrated to provide an adaptive secure communication solution for protecting sensitive information.
