[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/dFHzWErq)

# Resume Analysis System

## Description

This project implements a resume analysis system that uses formal language theory to process, classify, and evaluate candidates based on their resumes and job descriptions. The system applies regular expressions, deterministic finite automata (DFA), finite state transducers (FST), and context-free grammars (CFG) to perform a comprehensive and structured analysis.

## Team

- Cristian Molina
- Santiago Morales
- Carlos Felipe Sanchez

## Project Structure



```
resume-screening-system/
├── data/
│   └── sample_resumes/  # Sample resumes for testing
├── output/
│   └── summaries/  # Generated analysis results
├── src/
│   ├── config/
│   │   └── regex_config.py  # Regular expression configuration
│   ├── models/
│   │   ├── resume_parser.py  # Processing and information extraction
│   │   ├── resume_classifier.py  # Classification using finite automata
│   │   ├── resume_ranker.py  # Evaluation using transducers
│   │   └── resume_grammar.py  # Validation using context-free grammars
│   └── main.py  # System entry point
├── docs/  # Project documentation
└── README.md  # This file
```

## Requirements

- Python 3.10+
- Required libraries (installable via `requirements.txt` file):
  - textx
  - pyformlang
  - python-docx
  - PyPDF2
  - tkinter

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/Bloque-CED/ti1-2025-1-e6-unionmagdalena.git
   ```


2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```


3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```


## Usage

### Command Line Interface

Run the main program:

```
python src/main.py
```


The program will present an interactive menu with the following options:
1. Use a predefined sample resume
2. Upload your own resume file
3. Exit

### Resume Processing

1. Select a resume (predefined or uploaded)
2. Choose a role for evaluation (Data Scientist, AI Engineer, Software Engineer, Web Developer, DevOps Engineer)
3. The system will process the resume and display:
   - Classification using DFA
   - Detailed scoring and ranking using FST
   - Links to the generated summary files (HTML and Markdown)

## Supported Roles

- Data Scientist
- AI Engineer
- Software Engineer
- Web Developer
- DevOps Engineer

## Supported File Formats

- PDF (.pdf)
- Microsoft Word (.docx)
- Plain text (.txt)
