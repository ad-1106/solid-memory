import os
import csv
import google.generativeai as genai
import json
# Configure Gemini
genai.configure(api_key="AIzaSyCTl3ZLH-GeSmN64p2ffioKXnBu3_Vfxok")
model = genai.GenerativeModel("gemini-2.5-flash")  # or "gemini-1.5-pro"

csv_file = open("/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/Images/data.csv",'w')
writer = csv.writer(csv_file)
writer.writerow(['Path to image','x_cooridnte','y_coordinate',"object_name",'paragraph_1','paragraph_2','paragraph_3','map_path''anomaly_detected','camera'])
file_original = os.listdir("/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/ProcessedImages")
files=[] 
watchDirectory = "/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/ProcessedImages"
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
print(file_original)
for file_name in file_original:
    if any(file_name.lower().endswith(ext) for ext in image_extensions):
        files.append(file_name)

for file in files:
    camera = ""
    first_letter = file[0].lower()
    if first_letter == 'b':
        camera = "Back Camera"
    elif first_letter == 'f':
        camera = "Front Camera"
    elif first_letter == 'r':
        camera = "Right Camera"
    elif first_letter == "l":
        camera = "Left Camera"
    parts = file.split("_")   # fixed: should use file, not files
    x_coordinate = [p for p in parts if p.startswith("x=")][0].split("=")[1]
    y_coordinate = [p for p in parts if p.startswith("y=")][0].split("=")[1]
    content=""
    file_path = watchDirectory + '/' + file
    print(file_path)
    prompt = """ou are an advanced AI system specializing in Mars surface exploration and anomaly detection for autonomous rover missions. Your primary function is to analyze images from Mars rovers operating in marsyard environments and provide detailed assessments of detected anomalies and landmarks.

**CRITICAL MISSION CONTEXT:**
You are analyzing images from a rover in a Mars-analog environment (marsyard). You must be EXTREMELY STRICT in identification to avoid false positives. According to mission rulebook: mechanical tools, electronic tools, building structures are LANDMARKS (not anomalies).

**ABSOLUTE RULE: SHADOWS ARE NEVER DETECTIONS**
NEVER detect shadows, dark areas, or lighting effects as any type of object. Shadows are completely prohibited from detection.

**OUTPUT FORMAT:**
Respond in JSON format only:

**FOR ANOMALIES:**

{“anomaly_detected”: true,“landmark_detected”: false,“object_name”: “Descriptive name of the detected anomaly”,“paragraph_1”: “Physical Description & Context - 80-120 words”,“paragraph_2”: “Anomaly Classification & Scientific Rationale - 80-120 words”,“paragraph_3”: “Scientific Value & Mission Implications - 80-120 words”}


**FOR LANDMARKS:**

{“anomaly_detected”: false,“landmark_detected”: true,“object_name”: “Descriptive name of the detected landmark”,“paragraph_1”: “Physical Description & Context - 80-120 words”,“paragraph_2”: “Landmark Classification & Purpose - 80-120 words”,“paragraph_3”: “Navigation Value & Reference Utility - 80-120 words”}


**FOR NEITHER:**
{“anomaly_detected”: false,“landmark_detected”: false, “object_name”: “nothing”,“paragraph_1”: “Physical Description & Context - 80-120 words”,“paragraph_2”: “Landmark Classification & Purpose - 80-120 words”,“paragraph_3”: “Navigation Value & Reference Utility - 80-120 words”}



**ABSOLUTE SHADOW PROHIBITION:**

**NEVER DETECT SHADOWS AS:**
- ArUco markers (even if shadow appears rectangular)
- Tools or equipment
- Human figures
- Building structures
- Any type of landmark or anomaly

**SHADOW IDENTIFICATION:**
Shadows appear as:
- Dark areas cast by objects blocking light
- Areas with reduced illumination
- Dark patches on ground or surfaces
- Black or very dark regions without physical substance
- Areas that change darkness based on lighting angle
- Dark shapes that are projections of real objects

**SHADOW REJECTION CHECKLIST:**
Before detecting anything, ask:
✓ Is this just a dark area due to lighting?
✓ Could this be a shadow cast by another object?
✓ Does this have physical substance or just reduced light?
✓ Would this disappear with different lighting conditions?
✓ Is this darker than surroundings due to blocked light?

**If ANY answer suggests shadow → IMMEDIATELY REJECT**

**ULTRA-STRICT ARUCO MARKER DETECTION:**

ArUco markers must meet ALL criteria with NO shadow possibility:

1. **Physical Object**: Must be a real physical marker, NOT a shadow
2. **Perfect Square Shape**: Four clear, straight edges forming perfect square
3. **Black Border**: Solid black border (NOT shadow darkness)
4. **White Interior**: Clean white background (NOT just lighter area)
5. **Visible Internal Pattern**: Clear black geometric pattern inside white area
6. **Physical Substance**: Must be an actual marker object, not lighting effect
7. **Consistent Under Different Lighting**: Would remain visible regardless of light direction

**ARUCO ANTI-SHADOW VERIFICATION:**
✓ Can I see this is a physical marker object (not shadow)?
✓ Does it have actual black and white materials (not light/dark areas)?
✓ Is the border real black material (not shadow edge)?
✓ Is the white area actual white material (not illuminated ground)?
✓ Would this marker exist regardless of sun position?

**LANDMARK DETECTION CRITERIA:**

**Mechanical Tools (landmark_detected: true):**
- Physical tools with actual substance: wrenches, screwdrivers, hammers
- Must have visible material construction (metal, plastic, etc.)
- NOT dark shapes that could be shadows of tools
- Clear three-dimensional form visible

**Electronic Tools (landmark_detected: true):**
- Physical devices with visible components: sensors, displays, circuits
- Must show actual material construction
- NOT dark rectangular areas that could be shadows
- Evidence of manufactured materials and components

**Building Structures (landmark_detected: true):**
- Physical constructed elements: walls, frames, supports
- Must show actual building materials and construction
- NOT dark areas between objects that could be shadows
- Clear evidence of human construction and engineering

**ANOMALY DETECTION CRITERIA:**

**Human Presence (anomaly_detected: true):**
- Actual human figures with biological characteristics
- Must show real clothing, skin, body parts
- NOT dark human-shaped shadows
- Clear evidence of living person presence

**COMPREHENSIVE REJECTION CRITERIA:**

**NEVER DETECT (Automatic Rejection):**
1. **All Shadows**: Dark areas, reduced lighting, cast shadows
2. **Natural Terrain**: Rocks, stones, geological formations of any type
3. **Lighting Effects**: Bright spots, dark spots, reflections, glare
4. **Unclear Objects**: Blurry, distant, ambiguous shapes
5. **Natural Patterns**: Random dark/light areas, soil variations
6. **Ground Textures**: Surface variations, dirt patterns, natural markings

**SHADOW-SPECIFIC REJECTION EXAMPLES:**
- Dark rectangular areas on ground (shadow, not ArUco marker)
- Human-shaped dark areas (shadow, not person)
- Dark tool-like shapes (shadows of tools, not actual tools)
- Dark structural shapes (shadows between buildings, not structures)
- Any dark area that could be blocked light

**DECISION PROCESS:**
1. **Is this a shadow or lighting effect?** → REJECT IMMEDIATELY
2. **Is this clearly natural terrain?** → REJECT
3. **Is this a physical artificial object with substance?** → Consider detection
4. **Can I identify specific material construction?** → Proceed with classification
5. **Any uncertainty about physical reality?** → REJECT

**CRITICAL ANTI-FALSE-POSITIVE MEASURES:**

- **Shadow Detection = Immediate Failure**: Never classify shadows as anything
- **Material Evidence Required**: Must see actual physical materials
- **Lighting Independence**: Object must exist regardless of lighting conditions
- **Physical Substance**: Must have actual three-dimensional form
- **When in Doubt**: Always reject rather than risk false positive

**QUALITY STANDARDS:**
- Zero tolerance for shadow detection
- Physical substance required for all detections
- Material evidence must be visible
- Conservative approach mandatory
- Accuracy over detection rate

**FINAL INSTRUCTION:**
If there is ANY possibility an object could be a shadow, lighting effect, or natural formation, you MUST reject it. False positives, especially shadow detections, completely undermine mission credibility and waste critical resources.

Remember: Shadows have no physical substance and provide no scientific or navigational value. They are completely prohibited from detection under any circumstances.
"""
    # Gemini API call
    response = model.generate_content([prompt, {"mime_type": "image/png", "data": open(file_path, "rb").read()}])
    content = response.text.strip() if response.text else "No response"
    # A more robust way to extract the JSON
    try:
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = content[start:end]
            content_dict = json.loads(json_str)
        else:
            print(f"Could not find JSON in response for {file}")
            continue # Skip this file
    except json.JSONDecodeError:
        print(f"Failed to decode JSON for {file}. Response was:\n{content}")
        continue # Skip this file
    print((content_dict))
    if (content_dict["landmark_detected"] == False) :
       pass
    else:
        writer.writerow([file_path,x_coordinate,y_coordinate,content_dict["object_name"],content_dict["paragraph_1"],content_dict["paragraph_2"],content_dict["paragraph_3"],file_path.replace(".png",".jpeg"),content_dict["anomaly_detected"],camera])




import csv

# Initialize data structures
files = []
paragraph_1 = {}
paragraph_2 = {}
paragraph_3 = {}
x_coordinate = {}
y_coordinate = {}
object_name = {}
map_name = {}
anomaly_detected = {}
camera_name = {}

# Read data from the CSV file
try:
    with open("/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/Images/data.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 10:  # Ensure all columns are present
                file_name = row[0]
                files.append(file_name)
                x_coordinate[file_name] = row[1]
                y_coordinate[file_name] = row[2]
                paragraph_1[file_name] = row[4]
                paragraph_2[file_name] = row[5]
                paragraph_3[file_name] = row[6]
                map_name[file_name] = row[7]
                object_name[file_name] = row[3]
                if row[8].lower() == "true":
                  anomaly_detected[file_name] = "Anomaly"
                elif row[8].lower() == "false":
                  anomaly_detected[file_name] = "Non Anomaly"
                camera_name[file_name] = row[9]
            else:
                print(f"Skipping row due to missing data: {row}")

except FileNotFoundError:
    print("Error: The CSV file was not found. Please check the path.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()

# Start building the main LaTeX content string
latex_file = r"""\documentclass[a4paper,12pt]{report}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{top=2cm, bottom=2cm, left=2cm, right=2cm}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{float}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{amsmath}
\usepackage{hyperref}
\usepackage{multicol}
\usepackage{parskip}
\usepackage{array}
\usepackage{booktabs}
\setlength{\parindent}{0pt}

\begin{document}
%---------------------------
% Cover Page
%---------------------------
\begin{titlepage}
    \centering
    \vspace*{2cm}
    {\Huge\bfseries ERC 2025 \par}
    %% Logo
    \vspace*{2cm}
    \includegraphics[width=0.25\textwidth]{logo.png}\par\vspace{2cm}
    %% Main Title
    {\Huge\bfseries Report on detected landmarks \par}
    \vspace{1.5cm}
    %% Subtitle (optional)
    \vspace{2cm}
    %% Author and details
    {\large
        CRISS Robotics \par
        BITS Pilani,Pilani \par
         \par
    }
    \vfill
    %% Date
    {\large 26th August 2025\par}
\end{titlepage}

\clearpage

"""

# Loop through each file to generate its report page content
for file_name in files:
    par3_val = paragraph_3.get(file_name, 'No description available')
    par2_val = paragraph_2.get(file_name, 'No description available')
    par1_val = paragraph_1.get(file_name, 'No description available')
    x_val = x_coordinate.get(file_name, 'N/A')
    y_val = y_coordinate.get(file_name, 'N/A')
    map_val = map_name.get(file_name, 'N/A')
    obj_val = object_name.get(file_name, 'N/A')
    ano_val = anomaly_detected.get(file_name, 'N/A')
    cam_val = camera_name.get(file_name, 'N/A')
    latex_template_content = r"""
    \section*{Object Details}
    \textbf{Object Name:} %s \newline
    \textbf{Classification:} %s \newline
    \textbf{X Coordinate:} %s \newline
    \textbf{Y Coordinate:} %s \newline
    \textbf{Coordinate System:} Relative to Initial Position \newline
    \textbf{Camera:} %s\newline

    %% Images side-by-side
    \begin{figure}[H]
        \centering
        \begin{tabular}{@{}c@{\hspace{0.5cm}}c@{}}
            \includegraphics[width=0.45\linewidth]{%s} &
            \includegraphics[width=0.45\linewidth]{%s} \\
            \textbf{(a) Location Map} & \textbf{(b) Object Photograph}
        \end{tabular}
        \caption{Images of the map and the object}
        \label{fig:side_by_side}
    \end{figure}

    %% Object description section
    \section*{Object Description}
    \textbf{Physcial Description:} %s \newline\newline
    \textbf{Reason For Classification:} %s \newline\newline
    \textbf{Relevance to the mission:} %s 
    
    \clearpage
    """ % (obj_val,ano_val,x_val,y_val,cam_val,map_val,file_name,par1_val,par2_val,par3_val)
    
    latex_file += latex_template_content

# End the document after the loop
latex_file += r"\end{document}"

# Write the complete content to the .tex file
with open("report.tex", "w") as f:
    f.write(latex_file)
    # Generate the content for a single section. NO \documentclass or \begin{document}
