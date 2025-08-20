import csv

# Initialize data structures
files = []
description = {}
latitudes = {}
longitudes = {}
timestamps = {}

# Read data from the CSV file
try:
    with open("/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/Images/data.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 4:
                file_name = row[0]
                files.append(file_name)
                description[row[0]] = row[3]
                latitudes[row[0]] = row[1]
                longitudes[row[0]] = row[2]

            else:
                print(f"Skipping row due to missing data: {row}")

except FileNotFoundError:
    print("Error: The CSV file was not found. Please check the path.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()

# Start building the main HTML content string
full_report_content = ""

# Loop through each file to generate its report page content
for file_name in files:
    desc_val = description.get(file_name, 'No description available')
    lat_val = latitudes.get(file_name, 'N/A')
    lon_val = longitudes.get(file_name, 'N/A')
    ts_val = timestamps.get(file_name, 'N/A')

    # Generate a single-page report section for the current image
    page_html = f"""
  <main class="page" role="document">
    <header>
      <div class="mark" aria-hidden="true">
        <img src="/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/solid-memory/logo.jpg" alt="Organisation Logo" />
      </div>
      <div class="hgroup">
        <h1>Detected Objects</h1>
        <div class="meta">
          Date: <span id="report-date">2025-08-26</span> • Prepared by: <span id="prepared-by">CRISS Robotics</span>
        </div>
      </div>
    </header>

    <section style="margin-top:8px">
      <div class="card">
        <div class="card-h">1. Map Location</div>
        <div class="card-b">
          <figure class="figure" aria-label="Map showing the detected object's location"></figure>
          <div class="meta">Map showing the detected object</div>
        </div>
      </div>
    </section>

    <section>
      <div class="card">
        <div class="card-h">2. Image of Detected Object</div>
        <div class="card-b">
          <figure>
            <img id="object-image" src="{file_name}" alt="Photograph of the detected object"/>
            <figcaption class="meta">Detected Object</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section>
      <div class="card">
        <div class="card-h">3. Location Details</div>
        <div class="card-b">
          <div class="kv">
            <div class="k">Latitude</div><div id="lat">{lat_val}</div>
            <div class="k">Longitude</div><div id="lon">{lon_val}</div>
            <div class="k">Timestamp</div><div id="capture-ts">{ts_val}</div>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="card">
        <div class="card-h">4. Description</div>
        <div class="card-b">
          <p class="desc" id="description">
            {desc_val}
          </p>
        </div>
      </div>
    </section>

    <footer>
      This document is intended for ERC. Unauthorised distribution is prohibited. © <span id="year">2025</span> CRISS Robotics.
    </footer>
  </main>
"""
    full_report_content += page_html

# Now, put all the generated pages into one final HTML document
final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Detected Objects – Full Report</title>
  <style>
    :root{{
      --ink:#111111;--muted:#4b5563;--line:#e5e7eb;--brand:#0f172a;--accent:#1f2937;--bg:#ffffff;
    }}
    body{{margin:0;font-family: "Times New Roman", Times, Georgia, serif; color:var(--ink); background:var(--bg)}}
    .page{{width:auto; min-height:297mm; margin:10mm 20mm; padding:20mm; box-sizing:border-box; background:#fff; border:1px solid var(--line); display:flex; flex-direction:column; justify-content:flex-start}}
    header{{display:flex; gap:16px; align-items:center; padding-bottom:12px; border-bottom:2px solid var(--brand)}}
    .mark{{width:60px;height:60px; border-radius:12px; overflow:hidden; display:grid; place-items:center; background:#fff; border:1px solid var(--brand)}}
    .mark img{{width:100%; height:100%; object-fit:contain}}
    .hgroup{{flex:1}}
    h1{{margin:0; font-size:20px; letter-spacing:.2px}}
    h2{{margin:0 0 4px 0; font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:var(--accent)}}
    .meta{{margin-top:4px; color:var(--muted); font-size:12px}}
    .card{{border:1px solid var(--line); border-radius:8px; background:#fff; margin-top:10px}}
    .card > .card-h{{padding:6px 10px; border-bottom:1px solid var(--line); background:#f9fafb; font-weight:700; text-transform:uppercase; letter-spacing:.05em; font-size:11px; color:#1f2937}}
    .card > .card-b{{padding:10px; font-size:13px}}
    figure{{margin:0}}
    figure{{border:1px solid var(--line); background:#f8fafc; display:grid; place-items:center;}}
    figure img{{display:block; width:60vw;}}
    .kv{{display:grid; grid-template-columns: 90px 1fr; gap:4px 8px; font-size:13px}}
    .kv div{{padding:4px 0; border-bottom:1px dotted #e5e7eb}}
    .kv .k{{color:var(--muted)}}
    .desc{{font-size:13px; line-height:1.4; text-align:justify}}
    footer{{margin-top:auto; padding-top:6px; border-top:1px solid var(--line); color:var(--muted); font-size:10px; text-align:center}}
    @media print{{
      .page{{border:none; width:100%; min-height:100vh; padding:10mm; break-after: page;}}
      .card{{break-inside:avoid}}
      body{{background:#fff; margin:0}}
    }}
  </style>
</head>
<body>
  {full_report_content}
</body>
</html>"""

# Define the output file path
html_file_path = '/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/Images/results.html'

# Write the final HTML content to a single file
with open(html_file_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"\nHTML report generated at: {html_file_path}")