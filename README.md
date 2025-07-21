
## 📁 Mars Object Detection & Description Pipeline

This Python project automatically watches a directory for new images, sends those images to a local Ollama model for analysis, and writes the AI-generated descriptions to a CSV file.

## 📌 Purpose

This project is intended for use in image monitoring and analysis workflows, particularly for identifying and describing objects (e.g., those enclosed in yellow boxes) in image files. The description determines whether the object is typical in a Mars environment. The output is recorded in a structured `.csv` format.

---

## 🛠️ Features

- Watches a specified folder for new image files.
- Sends images to a vision-capable Ollama model (`qwen2.5vl:7b-q8_0`) for analysis.
- Receives a 50-word description starting with the object name.
- Determines if the object is typical in a Martian environment.
- Logs image path, object, and description to a CSV file.

---

## 🐍 Requirements

- Python 3.x  
- [`watchdog`](https://pypi.org/project/watchdog/)  
- [`ollama`](https://ollama.com/) with `qwen2.5vl:7b-q8_0` model installed and running  
- `csv` module (built-in)

Install dependencies:

```bash
pip install watchdog
````

---

## 📂 Directory Structure

```
/CRISS/Probation/
│
├── ProcessedImages/       # Watched directory (new images dropped here)
├── Images/
│   └── data.csv           # Output CSV file with detection data
├── your_script.py         # The Python script provided
```

---

## 🚀 How It Works

1. The script watches the `/ProcessedImages` directory for new image files.
2. When a new image is created, it sends the image to Ollama's vision model.
3. The model returns a 50-word paragraph beginning with the name of the object in the yellow box, followed by a brief contextual description and an assessment of its Martian relevance.
4. The script extracts:

   * Image path
   * First word (assumed object name)
   * Full description
5. These details are saved to `/Images/data.csv`.

---

## 🧠 Example Output

**CSV row:**

```
/full/path/to/image.jpg, ,Rover,Rover  A robotic rover designed for exploration, this object appears suited for a Martian environment...
```

---

## ▶️ Running the Script

Make sure your Ollama model is running:

```bash
ollama run qwen2.5vl:7b-q8_0
```

Then run the Python script:

```bash
python your_script.py
```

---

Let me know if you want this customized further (e.g., your name, logo, links to documentation, etc.).
```
