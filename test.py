#import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ollama import chat, AsyncClient
import csv
import asyncio
import os

file = open("/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/solid-memory/data.csv",'w')
writer = csv.writer(file)
writer.writerow(['Path to image','location','object_identified','description'])
file.close()
class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/ProcessedImages"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            source_path = event.src_path
            print("file created and processing")
            file = open("/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/Images/data.csv",'a')
            writer = csv.writer(file)
            async def chat():
                    content = ""
                    message = {'role': 'user', 'content': 'You are an intelligent assistant specialized in analyzing images from a Mars mission. Your task is to describe objects only if they are relevant anomalies or significant items related to the mission. Ignore and do not describe generic rocks, common geological formations, backgrounds, or anything that looks like ordinary terrain without unique features(DO NOT GENERATE ANY RESPONSE IN THIS CASE). Only generate a description when the object is unusual, scientifically interesting, or mission-relevant. generate a paragraph of 50 words that describes the object in view and state whether it is an item that is typical in a Mars environment. The first word should be what the object is, only the name of the object. If the name of the object contains multiple words, connect them with a hyphen. Do not use any punctuators as the first word. The first word should be the object that is detected in the image.', 'images': [source_path]}
                    async for part in await AsyncClient().chat(model='qwen2.5vl:7b-q8_0', messages=[message], stream=True):
                        reply+=part['message']['content']
                    print(content)
                    first_word = reply.split()[0]
                    if not content or not content.strip():
                        print(f"No meaningful response for {source_path}. Deleting image.")
                        os.remove(source_path)
                        return

                    lower_content = content.lower()
                    generic_phrases = [
                        "no anomaly", "nothing unusual", "ordinary terrain", "common rock",
                        "generic rock", "typical mars", "no significant object", "just rocks",
                        "empty scene", "nothing relevant"
                    ]
                    if any(phrase in lower_content for phrase in generic_phrases):
                        print(f"Generic/irrelevant description for {source_path}. Deleting image.")
                        os.remove(source_path)
                        return
                    writer.writerow([source_path,' ',first_word,reply.replace(first_word,"",1)])
                    file.close()
            asyncio.run(chat())
import csv
files = []
description={}
file = open("/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/solid-memory/data.csv",'r')
reader = csv.reader(file)
next(reader)
for row in reader:
        print(row[0])
        file_name = row[0]
        files.append(file_name)
        description[row[0]] = row[3]
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Processing Results</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #eef2f3, #dfe9f3);
            color: #333;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            font-size: 2.2em;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }}
        .stats {{
            max-width: 500px;
            margin: 0 auto 25px auto;
            padding: 15px;
            background: #ffffffcc;
            border-radius: 12px;
            text-align: center;
            font-size: 1.1em;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            padding: 10px;
        }}
        .image-card {{
            background: white;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }}
        .image-card:hover {{
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        .filename {{
            padding: 12px;
            font-weight: bold;
            background: #f7f9fa;
            font-size: 0.95em;
            color: #4a4a4a;
            border-bottom: 1px solid #ececec;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .image-card img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .description {{
            padding: 12px;
            font-size: 0.9em;
            color: #555;
            background: #fafbfc;
            border-top: 1px solid #f0f0f0;
            min-height: 50px;
        }}
        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.6em;
            }}
        }}
    </style>
</head>
<body>
    <h1>Image Processing Results</h1>
    <div class="stats">
        📊 Total images processed: {len(files)}
    </div>
    <div class="gallery">
"""

# Add image cards
for file_name in files:
    html_content += f"""
        <div class="image-card">
            <img src="{file_name}" alt="{file_name}">
            <div class="description">{description.get(file_name, 'No description available')}</div>
        </div>
    """

# Close HTML
html_content += """
    </div>
</body>
</html>
"""

# Save HTML file
html_file_path = '/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/Images/results.html'
with open(html_file_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\nHTML report generated at: {html_file_path}")

if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()