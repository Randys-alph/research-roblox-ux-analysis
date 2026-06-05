# A Data-Driven Approach to Evaluating User Experience in Metaverse: Sentiment Analysis and Telemetry Data on Roblox RPG vs Simulator

## Overview
This repository contains the dataset, analytical scripts, and supplementary materials for the research project evaluating the User Experience (UX) of contrasting game genres (RPG vs. Simulator) within the Roblox metaverse. 

By circumventing traditional manual surveys, this project employs a data-driven methodology that integrates objective telemetry data (extracted via the Roblox Web API) with unstructured electronic Word-of-Mouth (eWOM) gathered from Reddit. The analysis utilizes a dual-stream Natural Language Processing (NLP) pipeline encompassing VADER for real-time sentiment polarity classification and BERTopic for semantic topic clustering.

## Research Objects
* **RPG Representation:** *Blox Fruits*
* **Simulator Representation:** *Bee Swarm Simulator*

## Repository Structure
*Note: This repository is currently under active development. Data and scripts will be populated upon the commencement of the data collection phase.*

* `/data`
  * `/raw` - Unprocessed CSV files scraped from Reddit (r/bloxfruits, r/BeeSwarmSimulator) and raw JSON telemetry data.
  * `/processed` - Cleaned datasets following the dual-stream preprocessing pipeline.
* `/notebooks` - Jupyter Notebooks detailing the step-by-step exploratory data analysis (EDA) and model execution.
* `/src`
  * `scraper.py` - Python script utilizing the PRAW library for targeted Reddit thread extraction.
  * `preprocessing.py` - Script for text normalization (Lightweight cleaning for VADER; Deep cleaning & Lemmatization for BERTopic).
  * `nlp_engine.py` - Core algorithmic execution for VADER compound scoring and BERTopic clustering (all-MiniLM-L6-v2).
* `/results` - Output figures, semantic cluster visualizations, and statistical correlation tables.

## Methodology Pipeline
1. **Data Acquisition:** Extraction of the top 1,000 active discussion threads (January 2025 – May 2026) using Python Reddit API Wrapper (PRAW) and concurrent player metrics from Roblox API.
2. **Dual-Stream Preprocessing:** * *Sentiment Stream:* Retention of capitalization and punctuation for heuristic intensity measurement.
   * *Topic Modeling Stream:* Lowercasing, punctuation removal, stopword filtering, and lemmatization.
3. **NLP Execution:** * Sentiment Analysis using VADER (Valence Aware Dictionary and sEntiment Reasoner).
   * Topic Modeling using deep learning-based BERTopic.
4. **UX Synthesis:** Correlation mapping between objective telemetry retention and subjective semantic sentiment.

## Requirements
To replicate the environment and execute the scripts, the following primary dependencies are required:
* Python 3.8+
* pandas
* numpy
* praw
* vaderSentiment
* bertopic
* scikit-learn
* matplotlib / seaborn

## Authors
* **Randysta Rasta Putra** - *Computer Science Department, Bina Nusantara University*
* **Joy Rochelle Kartolo** - *Computer Science Department, Bina Nusantara University*

## License
This project is for academic and research purposes. Data extracted from Reddit and Roblox are subject to their respective API Terms of Service.
