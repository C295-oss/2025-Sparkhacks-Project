from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from bs4 import BeautifulSoup

import os
import webbrowser
import threading



# Yes, this could be done a better way, but I am on a time crunch
templates = [
"""
!# [name]
!### [Desc]

!p lorem ipsum dolor sit amet

!---
!## [Topic]

!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet

!---
!## [Topic]

!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet


!---
!## [Topic]

!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet


!---
!## [Topic]

!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
"""
,
"""
!# [Title]
!### [Desc]

!img [src]


!## [topic]

!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet

!----

!background_color black
!font_color white
"""
,
"""
!## [topic]
!### [desc]

!---

!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
!p lorem ipsum dolor sit amet
"""
]

app = FastAPI()


def start_http_server():
    os.chdir(os.path.dirname(os.path.abspath("index.html")))
    server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print(f"Serving at http://localhost:8000")
    server.serve_forever()  # This will run in a separate thread


def generateHTML(body, style):
    FILENAME="index.html"
    TITLE="Page"

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{TITLE}</title>
</head>
<style>
    body {{
          display: flex;
        flex-direction: column;
        align-items: center;
        height: 100vh;
        {style}
    }}
</style>
<body>
    {body}
</body>
</html>
"""

    try:
        with open(FILENAME, 'w', encoding='utf-8') as f:
            f.write(html_body)
        
        if not hasattr(generateHTML, "server_thread"):
                generateHTML.server_thread = threading.Thread(target=start_http_server, daemon=True)
                generateHTML.server_thread.start()
                webbrowser.open('http://localhost:8080')
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def createHtmlFileContent(parsedInfo):
    htmlBodyContent = []
    styleContent = []

    for command, data in parsedInfo:
        if command == "!#":
            htmlBodyContent.append(f"<h1>{data}</h1>")
        elif command == "!##":
            htmlBodyContent.append(f"<h2>{data}</h2>")
        elif command == "!###":
            htmlBodyContent.append(f"<h3>{data}</h3>")
        elif command == "!p":
            htmlBodyContent.append(f"<p>{data}</p>")
        elif command == "!img":
            htmlBodyContent.append(f'<img src="{data}" alt="image">')
        elif command == "!a":
            htmlBodyContent.append(f'<a href="{data}">Link</a>')
        elif command == "!br":
            htmlBodyContent.append("<br/>")
        elif command == "!---":
            htmlBodyContent.append("<hr/>")
        elif command == "!background_color":
            styleContent.append(f"background-color: {data};")
        elif command == "!font_color":
            styleContent.append(f"color: {data};")

    return ''.join(htmlBodyContent), ''.join(styleContent)


def parse(text: str):
    parsedInfo = []
    
    for line in text.splitlines():
        if line.startswith("!# "):
            parsedInfo.append(("!#", line[3:].strip()))
        elif line.startswith("!## "):
            parsedInfo.append(("!##", line[4:].strip()))
        elif line.startswith("!### "):
            parsedInfo.append(("!###", line[5:].strip()))
        elif line.startswith("!p "):
            parsedInfo.append(("!p", line[3:].strip()))
        elif line.startswith("!img "):
            parsedInfo.append(("!img", line[5:].strip()))
        elif line.startswith("!a "):
            parsedInfo.append(("!a", line[3:].strip()))
        elif line.startswith("!br"):
            parsedInfo.append(("!br", None))
        elif line.startswith("!---"):
            parsedInfo.append(("!---", None))
        elif line.startswith("!background_color "):
            parsedInfo.append(("!background_color", line[17:].strip()))
        elif line.startswith("!font_color "):
            parsedInfo.append(("!font_color", line[11:].strip()))
        else:
            print(f"Unknown command: {line}")

    return parsedInfo


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Only allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {"SERVER IS RUNNING :)"}


@app.get('/visualize/{text}')
async def visualize(text: str):
    print("generate()")
    print("Parsing. Calling function...")

    try: 
        result = parse(text)
        htmlCode, styleCode = createHtmlFileContent(result)
        generateHTML(htmlCode, styleCode)

        # Read the generated HTML file and return it as a response
        with open("index.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        return HTMLResponse(html_content)

    except Exception as e:
        return {"error": str(e)}


@app.get('/getHTML', response_class=HTMLResponse)
async def get_html():    
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.readlines()
        
        print(html_content)
        return HTMLResponse(html_content, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/generate_pdf')
async def gen_pdf():
    pass


@app.get('/template/{num}')
async def get_template(num: int):
    return templates[num-1]


@app.get('/generate/{text}', response_class=HTMLResponse)
async def generate(text: str):
    print("visualize()")
    print("Parsing. Calling function...")

    try:
        result = parse(text)
        htmlCode, styleCode = createHtmlFileContent(result)
        generateHTML(htmlCode, styleCode)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
