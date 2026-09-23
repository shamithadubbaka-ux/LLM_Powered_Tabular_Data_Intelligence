# LLM-Powered Tabular Data Intelligence

# Viva Questions and Answers

---

## 1. What is your project?

**Answer:**

My project is **LLM-Powered Tabular Data Intelligence**. It is an AI-assisted system that helps users analyze tabular datasets using automated data profiling, data-quality checks, natural-language queries, LLM-assisted SQL generation, and controlled query execution.

---

## 2. Why did you choose this project?

**Answer:**

Tabular data is widely used in organizations, but analyzing it often requires knowledge of SQL, programming, and statistics. I chose this project to combine traditional data analytics with Large Language Models and provide a simpler natural-language interface for exploring structured data.

---

## 3. What is a tabular dataset?

**Answer:**

A tabular dataset is structured data organized into rows and columns. Examples include CSV files, Excel spreadsheets, and relational database tables.

---

## 4. What is an LLM?

**Answer:**

LLM stands for **Large Language Model**. It is a machine-learning model trained on large amounts of text data and capable of understanding and generating natural language.

In this project, the LLM is used mainly to understand user questions and assist with analytical query generation.

---

## 5. Why use an LLM in a data-analysis system?

**Answer:**

An LLM allows users to interact with data using natural language instead of requiring them to write every query manually.

For example, a user can ask:

```text
Show total sales by region.
```

The LLM can help translate that request into an analytical query.

---

## 6. Does the LLM directly analyze the dataset?

**Answer:**

Not necessarily. The architecture separates language understanding from deterministic data processing.

The LLM interprets the request and can generate an analytical query, while the data engine performs the actual data operation.

This separation improves control and reliability.

---

## 7. What is data profiling?

**Answer:**

Data profiling is the process of examining a dataset to understand its structure, quality, and characteristics.

It can include:

* Number of rows.
* Number of columns.
* Data types.
* Missing values.
* Unique values.
* Duplicate records.
* Statistical information.

---

## 8. What is data quality?

**Answer:**

Data quality refers to how suitable data is for its intended purpose.

Common quality problems include:

* Missing values.
* Duplicate records.
* Invalid values.
* Incorrect data types.
* Inconsistent data.

---

## 9. Why is data-quality checking important?

**Answer:**

Poor-quality data can produce incorrect analytical results. Therefore, identifying quality problems before analysis helps users understand limitations in the dataset.

---

## 10. What is SQL?

**Answer:**

SQL stands for **Structured Query Language**. It is used to interact with relational databases and perform operations such as filtering, grouping, joining, inserting, updating, and retrieving data.

---

## 11. What is text-to-SQL?

**Answer:**

Text-to-SQL is the process of converting a natural-language request into an SQL query.

For example:

```text
Find the average sales by region.
```

can be converted into:

```sql
SELECT region, AVG(sales)
FROM sales
GROUP BY region;
```

---

## 12. Why do you need an SQL Guard?

**Answer:**

LLM-generated SQL should not automatically be trusted. An SQL Guard provides a validation layer that can reject potentially dangerous operations.

For an analytics application, commands such as:

```text
DROP
DELETE
UPDATE
INSERT
ALTER
TRUNCATE
```

can be restricted.

---

## 13. What happens if the LLM generates an incorrect query?

**Answer:**

The query can fail validation or execution. The system can return an error instead of blindly executing it.

The architecture should also provide appropriate error handling and, where implemented, allow the query-generation process to be corrected or retried.

---

## 14. Why use Python?

**Answer:**

Python provides strong libraries for data analysis, machine learning, APIs, and AI integration. Libraries such as Pandas make tabular-data processing convenient.

---

## 15. Why use Pandas?

**Answer:**

Pandas provides DataFrame-based data structures and functions for loading, filtering, transforming, aggregating, and analyzing tabular data.

---

## 16. What is a DataFrame?

**Answer:**

A DataFrame is a two-dimensional tabular data structure provided by Pandas. It consists of rows and columns and is commonly used for data analysis.

---

## 17. What are missing values?

**Answer:**

Missing values are entries where information is unavailable or not recorded.

For example:

```text
Name    Age
John    21
Alice
Bob     23
```

The missing age for Alice is a missing value.

---

## 18. What are duplicate records?

**Answer:**

Duplicate records are repeated rows containing the same or substantially identical information.

Duplicates can affect calculations and should therefore be identified during data-quality analysis.

---

## 19. What is natural-language processing?

**Answer:**

Natural Language Processing, or NLP, is a field of AI concerned with enabling computers to understand and process human language.

In this project, NLP capabilities help interpret natural-language data questions.

---

## 20. What is the role of the Data Engine?

**Answer:**

The Data Engine performs the actual data operations.

Its responsibilities include:

* Loading datasets.
* Filtering data.
* Performing aggregations.
* Running analytical operations.
* Returning results.

---

## 21. What is the difference between the LLM and the Data Engine?

**Answer:**

The LLM focuses on understanding language and generating analytical instructions, while the Data Engine performs the actual data processing.

The LLM is the intelligence/interface layer, while the Data Engine is the execution layer.

---

## 22. Why should the LLM not have unrestricted database access?

**Answer:**

An LLM can generate incorrect or unintended commands. Giving it unrestricted access could create security and data-integrity risks.

A controlled architecture with validation and limited database permissions reduces these risks.

---

## 23. What is the purpose of `.env`?

**Answer:**

The `.env` file can store configuration values and sensitive environment-specific information such as API keys.

Sensitive information should not be committed to a public GitHub repository.

---

## 24. Why is `.gitignore` important?

**Answer:**

`.gitignore` tells Git which files should not be tracked.

For this project, it can be used to exclude:

```text
.env
.venv/
__pycache__/
*.pyc
```

This helps prevent sensitive information and unnecessary generated files from being uploaded.

---

## 25. What are the main modules in your project?

**Answer:**

The main modules are:

```text
main.py
config.py
data_engine.py
profiling.py
quality.py
sql_guard.py
llm.py
```

Each module has a separate responsibility, making the project easier to maintain.

---

## 26. What is modular programming?

**Answer:**

Modular programming divides an application into smaller independent components or modules.

For example, profiling and SQL validation are separated into different modules instead of placing all functionality in one large file.

---

## 27. What is the advantage of modular architecture?

**Answer:**

It improves:

* Maintainability.
* Testing.
* Debugging.
* Reusability.
* Extensibility.

It also makes it easier to replace or upgrade individual components.

---

## 28. Can your project work without an LLM?

**Answer:**

The deterministic components such as data loading, profiling, quality checks, and direct analysis can work without an LLM.

However, the natural-language interaction and LLM-assisted query generation features specifically require an LLM or another language-understanding mechanism.

---

## 29. What are the limitations of your project?

**Answer:**

Important limitations include:

* LLM-generated queries may be incorrect.
* Poor-quality input data can affect results.
* Complex questions may require additional validation.
* Large datasets may require more powerful processing infrastructure.
* External LLM APIs can introduce latency or service dependencies.

---

## 30. How can the project be improved?

**Answer:**

Future improvements could include:

* Automated visualizations.
* Retrieval-Augmented Generation.
* Vector search.
* Data lineage.
* Enterprise data catalogs.
* Cloud data warehouse integration.
* Role-based access control.
* Advanced anomaly detection.
* Query optimization.

---

## 31. What is RAG?

**Answer:**

RAG stands for **Retrieval-Augmented Generation**.

It combines information retrieval with an LLM. Relevant information is retrieved from a knowledge source and provided to the model as context before generating a response.

---

## 32. How could RAG be used in your project?

**Answer:**

RAG could retrieve dataset documentation, business definitions, column descriptions, data dictionaries, or organizational guidelines.

The retrieved context could then help the LLM generate more appropriate analytical queries.

---

## 33. What is a vector database?

**Answer:**

A vector database stores numerical vector representations called embeddings and allows similarity-based retrieval.

It can be useful for semantic search and RAG systems.

---

## 34. What is data lineage?

**Answer:**

Data lineage describes the movement and transformation of data from its source to its final output.

For example:

```text
Source Dataset
      ↓
Transformation
      ↓
SQL Query
      ↓
Analysis
      ↓
Result
```

---

## 35. What happens when a user asks a question?

**Answer:**

The general workflow is:

```text
User Question
      ↓
LLM Interpretation
      ↓
Query Generation
      ↓
SQL Validation
      ↓
Data Engine
      ↓
Result
      ↓
Human-Readable Explanation
```

---

## 36. Give an example of a user query.

**Answer:**

A user could ask:

```text
Which region generated the highest total revenue?
```

The system can interpret the question, generate an appropriate aggregation query, validate it, execute it, and present the resulting values.

---

## 37. What makes your project different from a normal SQL application?

**Answer:**

A traditional SQL application generally requires users to formulate SQL queries directly.

This project adds a natural-language interaction layer using an LLM, while retaining deterministic data processing and SQL validation underneath.

---

## 38. What makes your project different from simply asking an LLM about data?

**Answer:**

The project does not rely only on the LLM's generated answer.

It combines:

```text
LLM
+
SQL Validation
+
Data Engine
+
Data Profiling
+
Data Quality Analysis
```

The actual dataset operations are performed by the application's data-processing layer.

---

## 39. What happens if the dataset contains incorrect data?

**Answer:**

The system can identify potential quality issues such as missing values, duplicates, inconsistent types, or unusual values.

However, detecting an issue does not automatically mean that the value is wrong. Domain-specific validation may still be required.

---

## 40. What is the main contribution of your project?

**Answer:**

The main contribution is an architecture that combines natural-language interaction through an LLM with controlled, deterministic tabular-data processing.

It demonstrates how AI can assist data analysis without giving the language model unrestricted control over the underlying data.

---

# Quick Revision Questions

## One-Line Answers

### What does LLM stand for?

Large Language Model.

### What does SQL stand for?

Structured Query Language.

### What does NLP stand for?

Natural Language Processing.

### What does RAG stand for?

Retrieval-Augmented Generation.

### What is Pandas?

A Python library widely used for data manipulation and analysis.

### What is a DataFrame?

A two-dimensional tabular data structure used for data analysis.

### What is data profiling?

Automated examination of a dataset's structure and characteristics.

### What is data quality?

The degree to which data is suitable, accurate, complete, consistent, and usable for its intended purpose.

### What is text-to-SQL?

Converting natural-language questions into SQL queries.

### What is SQL Guard?

A validation layer that restricts unsafe or unwanted SQL operations.

### Why use `.gitignore`?

To prevent specified files such as secrets and generated files from being tracked by Git.

### Why use `.env`?

To store environment-specific configuration and sensitive values outside the source code.

---

# Final Viva Explanation

If the examiner asks:

**"Explain your project in one minute."**

You can answer:

> My project is called **LLM-Powered Tabular Data Intelligence**. The main objective is to make tabular-data analysis easier using Large Language Models. The system accepts a structured dataset and first performs data profiling and quality analysis to understand the data. Users can then ask questions about the dataset using natural language. The LLM interprets the question and can generate an analytical SQL query. Before execution, the query passes through an SQL Guard that checks for potentially unsafe operations. The validated query is then handled by the Data Engine, which performs the actual data analysis and returns the result. The main idea is to combine the natural-language capabilities of LLMs with deterministic data-processing and validation techniques rather than giving the LLM unrestricted access to the data.
