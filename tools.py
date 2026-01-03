import os
import requests
from crewai.tools import BaseTool

# Tool 1: Search the Internet (Simulates searching Knowledge Base)
class SearchTool(BaseTool):
    name: str = "Search Knowledge Base"
    description: str = "Useful to search for technical solutions and documentation."

    def _run(self, query: str) -> str:
        url = "https://google.serper.dev/search"
        payload = str({ "q": query })
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            return response.text
        except Exception as e:
            return f"Error searching: {str(e)}"

# Tool 2: Save Documentation (Simulates Google Drive)
class FileSaveTool(BaseTool):
    name: str = "Save Documentation"
    description: str = "Saves the documentation to a local file."

    def _run(self, content: str) -> str:
        # We will save it to a file named 'support_docs.md'
        try:
            with open("support_docs.md", "a") as f:
                f.write("\n\n---\n\n" + content)
            return "Successfully saved documentation to support_docs.md"
        except Exception as e:
            return f"Error saving file: {str(e)}"