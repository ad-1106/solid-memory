import pandas as pd
import os
from datetime import datetime
import re
import pdflatex
def clean_latex_string(text):
    """Clean text for LaTeX compatibility"""
    if pd.isna(text):
        return ""
    
    text = str(text)
    # Replace common problematic characters
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('^', '\\^{}')
    text = text.replace('~', '\\~{}')
    return text

def extract_filename_from_path(path):
    """Extract filename from full path"""
    if pd.isna(path):
        return ""
    return os.path.basename(str(path))

def generate_anomaly_pages(df):
    """Generate individual anomaly pages from CSV data"""
    anomaly_pages = ""
    
    for idx, row in df.iterrows():
        # Extract and clean data
        image_path = clean_latex_string(row.get('Path to image', ''))
        filename = extract_filename_from_path(image_path)
        location = clean_latex_string(row.get('location', ''))
        object_identified = clean_latex_string(row.get('object_identified', ''))
        description = clean_latex_string(row.get('description', ''))
        
        # Generate anomaly ID (you can customize this logic)
        anomaly_id = f"A{idx+1:03d}"
        
        # Determine category based on object type (you can customize this logic)
        category = "UNKNOWN"
        subcategory = "general"
        if "helmet" in object_identified.lower():
            category = "USEFUL"
            subcategory = "safety_equipment"
        elif "rover" in object_identified.lower():
            category = "USEFUL"
            subcategory = "vehicles_equipment"
        
        anomaly_page = f"""
\\vspace{{2em}}
\\noindent
\\textbf{{Anomaly \\#{idx+1} --- ID: {anomaly_id} }}

\\begin{{itemize}}[leftmargin=1.7cm]
    \\item \\textbf{{Type:}} {object_identified}
    \\item \\textbf{{Category:}} {category}
    \\item \\textbf{{Subcategory:}} {subcategory}
    \\item \\textbf{{Coordinates (X, Y, Z):}} {location if location else "Not specified"}
    \\item \\textbf{{Detection Time:}} \\underline{{\\hspace*{{3.5cm}}}}
    \\item \\textbf{{Confidence:}} \\underline{{\\hspace*{{2.3cm}}}}
    \\item \\textbf{{Duplication Status:}} \\underline{{\\hspace*{{3cm}}}}
\\end{{itemize}}

\\vspace{{0.7em}}
\\noindent \\textbf{{Cropped Visual Evidence:}}
\\begin{{center}}
\\fbox{{
    \\parbox{{0.75\\textwidth}}{{
        \\centering
        \\vspace{{0.5cm}}
        \\textit{{Image: {filename}}}
        \\vspace{{0.5cm}}
        
        % Uncomment the line below and replace with actual image path if images are available
        % \\includegraphics[width=0.7\\textwidth]{{{image_path}}}
        
        \\vspace{{1.5cm}}
    }}
}}
\\end{{center}}

\\vspace{{1em}}
\\noindent \\textbf{{Contextual Map/Location:}}
\\begin{{center}}
\\fbox{{
    \\parbox{{0.75\\textwidth}}{{
        \\centering
        \\vspace{{1.8cm}}
        \\textit{{Insert anomaly map, cropped scan, or image.}}
        \\vspace{{1.8cm}}
    }}
}}
\\end{{center}}

\\vspace{{1em}}
\\noindent \\textbf{{Detailed Description:}} \\\\
{description}

\\newpage
"""
        anomaly_pages += anomaly_page
    
    return anomaly_pages

def generate_anomaly_table(df):
    """Generate the master anomaly table"""
    table_rows = ""
    
    for idx, row in df.iterrows():
        object_identified = clean_latex_string(row.get('object_identified', ''))
        location = clean_latex_string(row.get('location', 'Not specified'))
        description = clean_latex_string(row.get('description', ''))
        
        # Truncate description for table
        short_desc = description[:50] + "..." if len(description) > 50 else description
        
        anomaly_id = f"A{idx+1:03d}"
        category = "USEFUL" if object_identified else "UNKNOWN"
        
        table_row = f"{idx+1} & {anomaly_id} & {object_identified} & {category} & general & {location} & 0.95 & None & {short_desc} \\\\\n\\hline\n"
        table_rows += table_row
    
    return table_rows

def create_latex_document(csv_file_path, output_file_path="criss_report_generated.tex"):
    """Main function to create the complete LaTeX document"""
    
    # Read CSV file
    try:
        df = pd.read_csv(csv_file_path)
        print(f"Successfully read CSV with {len(df)} rows")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Generate dynamic content
    anomaly_pages = generate_anomaly_pages(df)
    anomaly_table_rows = generate_anomaly_table(df)
    total_anomalies = len(df)
    
    # Get current date
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Complete LaTeX document
    latex_document = f"""\\documentclass[12pt,a4paper]{{report}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{graphicx}}
\\usepackage{{hyperref}}
\\usepackage{{fancyhdr}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{tabularx}}
\\usepackage{{lscape}}
\\usepackage[dvipsnames]{{xcolor}}
\\usepackage{{tcolorbox}}
\\usepackage{{enumitem}}
\\usepackage{{tikz}}

% --- Watermark setup ---
\\usepackage{{transparent}}
\\usepackage{{eso-pic}}
\\newcommand\\BackgroundPic{{
    \\put(0,0){{
    \\parbox[b][\\paperheight]{{\\paperwidth}}{{
      \\vfill
      \\centering
      \\transparent{{0.06}}
      \\resizebox{{0.95\\textwidth}}{{!}}{{
      \\scalebox{{2.1}}{{\\Huge\\sf CRISS ROBOTICS -- BITS Pilani}}
      }}
      \\vfill
    }}
  }}
}}

% --- Header & footer ---
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{CRISS ROBOTICS REPORT}}
\\fancyhead[R]{{ERC 2025}}
\\fancyfoot[C]{{\\thepage}}

\\begin{{document}}

\\AddToShipoutPicture*{{\\BackgroundPic}}

% -----------------------------------------------------------------
% COVER PAGE

\\begin{{titlepage}}
    \\centering
    {{\\Huge \\bfseries ERC 2025 Rover Mission Report\\par}}
    \\vspace{{2cm}}
    % \\includegraphics[width=0.16\\textwidth]{{logo_placeholder}}\\\\[1.5cm]
    \\vspace{{1.5cm}}
    {{\\Large CRISS ROBOTICS\\\\BITS Pilani}}\\\\[0.8cm]

    \\begin{{tabular}}{{rl}}
            \\textbf{{Team Name:}} & CRISS ROBOTICS, BITS Pilani \\\\
            \\textbf{{Competition:}} & ERC 2025 Marsyard Challenge \\\\
            \\textbf{{Version:}} & 1.0 (Auto-Generated) \\\\
            \\textbf{{Report Date:}} & {current_date} \\\\
            \\textbf{{Total Anomalies:}} & {total_anomalies} \\\\
    \\end{{tabular}}

    \\vfill
    \\rule{{0.8\\textwidth}}{{0.8pt}} \\\\
    \\vspace{{0.5cm}}
    \\itshape
    Mission exploration, anomaly detection, and scientific insight powered by CRISS ROBOTICS.
\\end{{titlepage}}

\\clearpage

% -----------------------------------------------------------------
% TABLE OF CONTENTS
{{
    \\hypersetup{{linkcolor=black}}
    \\tableofcontents
    \\thispagestyle{{empty}}
    \\clearpage
}}

% -----------------------------------------------------------------
% EXECUTIVE SUMMARY

\\chapter{{Executive Summary}}
This report presents the automated analysis of {total_anomalies} detected anomalies during the ERC 2025 Marsyard Challenge mission. The mission data has been processed and compiled to provide comprehensive documentation of all identified objects and their characteristics.

Key highlights:
\\begin{{itemize}}
\\item Total anomalies detected: {total_anomalies}
\\item Automated classification and documentation completed
\\item Detailed visual evidence and descriptions provided for each detection
\\item Mission data successfully processed and analyzed
\\end{{itemize}}

% -----------------------------------------------------------------
% MISSION OVERVIEW

\\chapter{{Mission Overview}}
\\section{{Operational Context}}
\\vspace{{0.5em}}
\\noindent \\textbf{{Competition Slot:}} \\underline{{\\hspace{{4cm}}}}\\\\[0.5em]
\\noindent \\textbf{{Marsyard/Field Description:}} \\\\
\\textcolor{{gray}}{{Type your brief arena description here...}} \\\\[0.8em]
\\noindent \\textbf{{Mission Start Time:}} \\underline{{\\hspace{{3cm}}}}\\\\[0.5em]
\\noindent \\textbf{{Mission End Time:}} \\underline{{\\hspace{{3cm}}}}\\\\[0.5em]
\\noindent \\textbf{{Total Duration:}} \\underline{{\\hspace{{2.5cm}}}} min

\\section{{Travel Time and Distance Stats}}
\\vspace{{0.5em}}
\\noindent \\textbf{{Total Path Length:}} \\underline{{\\hspace{{2.5cm}}}} meters\\\\[0.5em]
\\noindent \\textbf{{Total Anomalies Detected:}} {total_anomalies}\\\\[0.5em]
\\noindent \\textbf{{Average Rover Speed:}} \\underline{{\\hspace{{2.5cm}}}} m/s\\\\[0.5em]
\\noindent \\textbf{{Number of Stops:}} \\underline{{\\hspace{{2cm}}}}

% -----------------------------------------------------------------
% ROVER PATH SUMMARY

\\chapter{{Rover Path Summary}}
\\section{{Path Visualization}}
\\vspace{{0.7em}}
Insert your MATLAB/Python path map or scan here.\\\\[1em]
\\noindent
\\begin{{center}}
\\fbox{{\\parbox{{0.82\\textwidth}}{{
    \\vspace{{1.5cm}}
    \\centering
    \\textit{{Drag or insert your trajectory image or exported map here.}}
    \\vspace{{1.5cm}}
}}}}
\\end{{center}}

\\section{{Waypoints Table}}

\\begin{{center}}
\\begin{{tabularx}}{{\\textwidth}}{{|c|X|X|X|X|X|}}
\\hline
\\textbf{{\\#}} & \\textbf{{Description}} & \\textbf{{Timestamp}} & \\textbf{{X}} & \\textbf{{Y}} & \\textbf{{Z}} \\\\
\\hline
1 & Start Position & & & & \\\\
2 & Waypoint 1 & & & & \\\\
... &  &  &  &  &  \\\\
n & End Position & & & & \\\\
\\hline
\\end{{tabularx}}
\\end{{center}}

% -----------------------------------------------------------------
% ANOMALY DETECTION & CLASSIFICATION

\\chapter{{Anomaly Detection \\& Classification Summary}}
\\section{{Master Anomaly Table}}

\\begin{{center}}
\\begin{{tabularx}}{{\\textwidth}}{{|c|c|c|c|c|c|c|c|X|}}
\\hline
\\textbf{{\\#}} & \\textbf{{Anomaly ID}} & \\textbf{{Type}} & \\textbf{{Category}} & \\textbf{{Subcategory}} & \\textbf{{Coordinates (X,Y,Z)}} & \\textbf{{Confidence}} & \\textbf{{Duplication Status}} & \\textbf{{Description/Notes}} \\\\
\\hline
{anomaly_table_rows}
\\end{{tabularx}}
\\end{{center}}

\\section{{Duplication Detection Table}}
\\begin{{center}}
\\begin{{tabularx}}{{0.8\\textwidth}}{{|c|c|c|c|X|}}
\\hline
\\textbf{{Primary ID}} & \\textbf{{Duplicate ID}} & \\textbf{{Distance (m)}} & \\textbf{{Resolution}} & \\textbf{{Remarks}} \\\\
\\hline
 & & & & \\\\
 & & & & \\\\
\\hline
\\end{{tabularx}}
\\end{{center}}

\\section{{Anomaly Category Distribution}}
\\vspace{{0.5em}}
Insert your pie/bar chart here for anomaly type and counts.\\\\
\\begin{{center}}
\\fbox{{\\parbox{{0.7\\textwidth}}{{\\centering\\vspace{{1cm}}\\textit{{Place chart or summary here.}}\\vspace{{1cm}}}}}}
\\end{{center}}

% -----------------------------------------------------------------
% DETAILED ANOMALY REPORTS

\\chapter{{Detailed Anomaly Reports}}

{anomaly_pages}

% -----------------------------------------------------------------
% PATH AND TRAVEL ANALYSIS

\\chapter{{Path and Travel Analysis}}
\\section{{Path Efficiency Charts}}
\\begin{{center}}
\\fbox{{
    \\parbox{{0.8\\textwidth}}{{
        \\centering
        \\vspace{{2cm}}
        \\textit{{Insert your speed/time path charts here (MATLAB/Python).}}
        \\vspace{{2cm}}
    }}
}}
\\end{{center}}

\\section{{Travel Summary Table}}
\\begin{{center}}
\\begin{{tabularx}}{{0.95\\textwidth}}{{|l|X|}}
\\hline
\\textbf{{Metric}} & \\textbf{{Value (to be typed)}} \\\\
\\hline
Total Distance Traveled         &  \\\\
Total Mission Duration (min)    &  \\\\
Average Speed (m/s)             &  \\\\
Number of Stops                 &  \\\\
Number of Anomalies Detected    & {total_anomalies} \\\\
Detection Rate (per min)        &  \\\\
\\hline
\\end{{tabularx}}
\\end{{center}}

% -----------------------------------------------------------------
% APPENDIX

\\appendix

\\chapter{{Appendix: Full Coordinate Data}}
\\begin{{landscape}}
\\begin{{longtable}}{{|c|c|c|c|c|c|c|c|c|c|c|c|}}
\\hline
\\textbf{{Timestamp}} & \\textbf{{Rover X}} & \\textbf{{Rover Y}} & \\textbf{{Rover Z}} & \\textbf{{Anomaly ID}} & \\textbf{{Anomaly X}} & \\textbf{{Anomaly Y}} & \\textbf{{Anomaly Z}} & \\textbf{{Type}} & \\textbf{{Category}} & \\textbf{{Confidence}} & \\textbf{{Notes}} \\\\
\\hline
% Add your full CSV data rows here if needed
\\end{{longtable}}
\\end{{landscape}}

\\chapter{{Appendix: Scripts Used}}
\\begin{{tcolorbox}}[colback=gray!10!white, colframe=gray!80!black, title=Python Processing Script]
\\begin{{verbatim}}
import pandas as pd
df = pd.read_csv('data.csv')
anomalies = df[df['object_identified'].notna()]
# Automated processing and LaTeX generation completed
print(f"Total anomalies processed: {{len(df)}}")
\\end{{verbatim}}
\\end{{tcolorbox}}

\\chapter{{Authorship and Acknowledgements}}
\\noindent\\textbf{{Team:}} CRISS Robotics, BITS Pilani\\\\
\\noindent\\textbf{{Report Generated:}} {current_date}\\\\
\\noindent\\textbf{{Processing Method:}} Automated CSV to LaTeX conversion\\\\

\\vspace{{0.8cm}}
\\noindent\\textit{{Brand watermark visible on every page.}}

\\end{{document}}"""

    # Write to file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(latex_document)
        print(f"LaTeX document successfully generated: {output_file_path}")
        print(f"Document contains {total_anomalies} anomaly pages")
        print("To compile: pdflatex criss_report_generated.tex")
    except Exception as e:
        print(f"Error writing LaTeX file: {e}")

# Usage example
if __name__ == "__main__":
    # Replace 'data.csv' with the path to your CSV file
    csv_file_path = "data.csv"
    output_file_path = "criss_report_generated.tex"
    
    create_latex_document(csv_file_path, output_file_path)
