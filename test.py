# import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ollama import chat 
import csv


file = open("/Users/todi/Documents/Code/Pythonprojects/CRISS/Probation/Images/data.csv",'w')
writer = csv.writer(file)
writer.writerow(['Path to image','location','object_identified','description'])

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
            stream = chat(
            model='qwen2.5vl:7b-q8_0',
            messages=[{'role': 'user', 'content': 'generate a paragraph of 50 words that describes the object in the yellow box and state wether it is an item that is typical in a Mars environment.The first word should be what the object is ', 'images': [source_path]}],
            stream=False,
        )
            print(stream['message']['content'])
            response = stream['message']['content']
            first_word = response.split()[0]
            writer.writerow([source_path,' ',first_word,response.replace(first_word," ",1)])

if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()