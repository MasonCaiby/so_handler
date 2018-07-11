import os

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

if __name__ == '__main__':
    notify("Creating and emailing Terry Pratchett text", "Im will let you know when I am done")
