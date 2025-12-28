#  Data Preprocessing for Nepali Subtitles

This repository contains preprocessing scripts for **Nepali subtitle datasets** used in training machine learning / deep learning models on video clips.  
The goal is to **clean, normalize, and standardize subtitle text** before feeding it into training pipelines.

---

##  Overview

The dataset consists of **subtitle files (SRT)** extracted from video clips.  
Since raw subtitles often contain noise and inconsistencies, this repository performs essential preprocessing steps such as:

- Removing unnecessary spaces and symbols
- Normalizing Nepali text
- Converting **Nepali numerals into words**
- Preparing clean text suitable for model training

---

##  Preprocessing Features

### Text Cleaning
- Removes extra spaces, punctuation, and unwanted symbols
- Normalizes subtitle text for consistency

###  Nepali Number to Words Conversion
Nepali numerals are converted into their **word equivalents**, which is crucial for NLP and speech-related tasks.

Examples:
- `१` → `एक`
- `१९९२` → `उन्नाइस सय बयानब्बे`

This ensures numerical consistency across the dataset.

---


