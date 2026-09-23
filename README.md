# LLM-Powered Tabular Data Intelligence

An AI-powered data intelligence system that analyzes tabular datasets, profiles data, detects quality issues, generates insights, and assists users with natural-language data analysis.

## Features

* Tabular dataset ingestion
* Automated data profiling
* Data quality assessment
* Missing-value and duplicate detection
* Statistical analysis
* Natural-language data queries
* SQL query generation and validation
* LLM-assisted data analysis
* Structured data insights

## Project Structure

```text
LLM_Powered_Tabular_Data_Intelligence/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── data_engine.py
│   ├── profiling.py
│   ├── quality.py
│   ├── sql_guard.py
│   └── llm.py
│
├── data/
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies

* Python
* Pandas
* SQL
* LLM
* Data Profiling
* Data Quality Analysis
* Natural Language Processing
* FastAPI / Streamlit

## How It Works

1. The user provides a tabular dataset.
2. The system loads and analyzes the dataset.
3. Data profiling is performed to understand columns, types, distributions, and missing values.
4. Data-quality checks identify potential problems.
5. Users can ask questions about the dataset using natural language.
6. The system generates and validates appropriate analytical operations or SQL queries.
7. The results are returned as understandable insights.

## Installation

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables in `.env`.

## Running the Project

Run the application using the project's main entry point.

```bash
python -m app.main
```

## Purpose

The project demonstrates how large language models can be combined with traditional data engineering and analytics techniques to make tabular data easier to explore and understand.
