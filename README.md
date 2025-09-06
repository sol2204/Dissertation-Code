# Dissertation-Code  

Python code for my undergraduate dissertation analyzing how **Chinese state media portrayed Japan in English (2013–2025)**.  

The project uses **LDA topic modeling** to identify themes, track their evolution, and explore how these connect to concepts of **strategic narratives**.  

---

## 📂 Project Structure  

The repository contains three Python scripts that form a complete pipeline:  

1. **URL Scraper**  
   - Scrapes URLs from the *People’s Daily* English-language website.  
   - Saves the results into a CSV file.  

2. **Article Scraper**  
   - Visits each URL from step 1.  
   - Extracts article text content.  
   - Saves the cleaned text and metadata (e.g., date, title) into a new CSV.  

3. **LDA Model**  
   - Reads in the dataset of articles.  
   - Preprocesses and tokenizes the text.  
   - Runs **Latent Dirichlet Allocation (LDA)** topic modeling.  
   - Identifies latent “topics” in the corpus, computes **coherence scores**, and prints top representative articles for each topic.  

---

## ⚙️ Dependencies  

- Python 3.8+  
- `pandas`  
- `numpy`  
- `nltk`  
- `gensim`  
- `pyLDAvis` (optional, for visualization)  

---
