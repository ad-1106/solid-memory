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
