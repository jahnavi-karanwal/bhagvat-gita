# Bhagavad Gita RAG System

## Overview

This project implements the retrieval component of a Retrieval-Augmented Generation (RAG) pipeline using the Bhagavad Gita as the knowledge source. The goal is to enable semantic search over Bhagavad Gita verses so that relevant teachings can be retrieved based on a user's query.

The current implementation focuses on data preparation, embedding generation, vector database construction, and retrieval of contextually relevant verses. Response generation and user interface development are planned for future stages.

---

## Objectives

* Build a searchable knowledge base from Bhagavad Gita verses.
* Convert textual content into vector embeddings for semantic understanding.
* Store embeddings in a vector database for efficient retrieval.
* Retrieve the most relevant verses for a given natural language query.
* Establish the foundation for a future RAG-powered spiritual guidance assistant.

---

## Dataset

This project uses the Bhagavad Gita dataset available on Hugging Face:

**Dataset:** JDhruv14/ Bhagavad-Gita_Dataset

The dataset contains all 701 verses of the Bhagavad Gita along with multilingual representations, enabling semantic search across scriptural content.

### Features

| Column   | Description                     |
| -------- | ------------------------------- |
| chapter  | Chapter number (1–18)           |
| verse    | Verse number within the chapter |
| sanskrit | Original Sanskrit verse         |
| hindi    | Hindi translation               |
| english  | English translation             |

### Dataset Statistics

* Total Verses: 701
* Chapters: 18
* Languages: Sanskrit, Hindi, English
* Format: CSV

For retrieval purposes, the English translations were used to generate embeddings and build a FAISS vector database for semantic similarity search.

---

## Project Workflow

### 1. Data Collection and Preprocessing

* Loaded Bhagavad Gita dataset using Pandas.
* Cleaned and formatted textual data.
* Combined relevant fields to create searchable text chunks.

### 2. Text Embedding Generation

* Generated dense vector embeddings using a Hugging Face embedding model.
* Converted verses into numerical representations suitable for semantic search.

### 3. Vector Database Creation

* Stored embeddings in a FAISS vector index.
* Enabled efficient similarity search across all Bhagavad Gita verses.

### 4. Semantic Retrieval

* Embedded incoming user queries.
* Performed similarity search against the vector database.
* Retrieved the most relevant verses and contextual information.

---

## Technologies Used

* Python
* Pandas
* LangChain
* Hugging Face Embeddings
* FAISS
* NumPy

---

## Current Progress

### Completed

* Dataset preprocessing
* Text chunk preparation
* Embedding generation
* FAISS vector store creation
* Similarity-based retrieval pipeline

### In Progress

* Retrieval evaluation
* Prompt engineering
* LLM integration

### Planned

* Complete RAG pipeline
* Context-aware response generation
* Streamlit-based user interface
* Conversational memory
* Deployment

---

## Sample Retrieval Flow

User Query

↓

Query Embedding

↓

FAISS Similarity Search

↓

Top-k Relevant Bhagavad Gita Verses

↓

Retrieved Context for Future LLM Generation

---

## Future Scope

The retrieved verses will be provided as context to a Large Language Model (LLM), enabling scripture-grounded responses that combine semantic retrieval with natural language generation. This will reduce hallucinations and improve the factual alignment of generated guidance with Bhagavad Gita teachings.

