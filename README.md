# A Data-Driven Approach to Evaluating User Experience in Metaverse: Sentiment Analysis and Telemetry Data on Roblox RPG vs Simulator

## Overview
This repository contains the dataset, analytical scripts, and supplementary materials for the research project evaluating the User Experience (UX) of contrasting game genres (RPG vs. Simulator) within the Roblox metaverse. 

Following the implementation of Reddit's "Responsible Builder Policy," this project utilizes a refined, adaptive methodology: bypassing traditional API wrappers in favor of direct JSON endpoint scraping. The analysis integrates objective telemetry data (Roblox Web API) with unstructured electronic Word-of-Mouth (eWOM) gathered from Reddit, processed via a dual-stream NLP pipeline (VADER & BERTopic).

## Research Objects
* **RPG Representation:** *Blox Fruits*
* **Simulator Representation:** *Bee Swarm Simulator*

## Repository Structure
* `/data`
  * `/raw` - Raw JSON dumps from Reddit and historical Roblox telemetry CSVs.
  * `/processed` - Final cleaned datasets, sentiment scores, and topic clustering results.
* `/src`
  * `/data_collection` - Scripts for direct JSON endpoint scraping and data merging.
  * `/preprocessing` - Text cleaning pipeline (Dual-stream: VADER vs. BERTopic).
  * `/analysis` - Scripts for VADER sentiment analysis and BERTopic topic modeling.

## Methodology Pipeline
1. **Data Acquisition:** Direct JSON endpoint scraping with sequential cursor-based pagination (Q2 2026), targeting the most recent discussion threads to ensure contemporary UX relevance.
2. **Dual-Stream Preprocessing:** * *Sentiment Stream:* Retention of capitalization and punctuation for VADER heuristic intensity measurement.
   * *Topic Modeling Stream:* Lowercasing, punctuation removal, stopword filtering, and lemmatization for BERTopic semantic clustering.
3. **NLP Execution:** * Sentiment Analysis using VADER (Valence Aware Dictionary and sEntiment Reasoner).
   * Topic Modeling using deep learning-based BERTopic (`all-MiniLM-L6-v2`).
4. **UX Synthesis:** Correlation mapping between objective telemetry retention metrics and subjective community sentiment patterns.

## Data Access
For transparency and reproducibility, the processed datasets used in this research are available for public access. 
You can download the complete dataset (CSV format) from the [GitHub Releases section of this repository](https://github.com/Randys-alph/research-roblox-ux-analysis/releases).

## Requirements
* Python 3.8+
* pandas, numpy, nltk
* vaderSentiment
* bertopic, sentence-transformers
* scikit-learn

## Authors
* **Randysta Rasta Putra** - *Computer Science Department, Bina Nusantara University*
* **Joy Rochelle Kartolo** - *Computer Science Department, Bina Nusantara University*

## License
This project is for academic and research purposes.
