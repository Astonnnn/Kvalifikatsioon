
import subprocess
import platform
import time
import re
import sys


def genereeri_valikvastustega_küsimus(teema):
    prompt = f"""Generate a multiple choice question about: {teema}.
Requirements:
-the output has to be on one line, with semicolons as separators
-the answer to the question has to be only one letter
-there is only one correct answer
-output follows this format: Q: Question; A) Answer1; B) Answer2; C) Answer3; D) Answer4; Correct Answer: (A/B/C/D)
"""
    if platform.system() == 'Windows':
        ollama_path = r'C:\Users\aston\AppData\Local\Programs\Ollama\ollama.exe'
    else:
        ollama_path = 'ollama'

    result = subprocess.run(
        [ollama_path, "run", "mistral"],
        input = prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='UTF-8'
    ) # kontrollib mis platform on ja siis saame mõlemad oma arvutis tööle
    print(result.stdout)
    return result.stdout

genereeri_valikvastustega_küsimus("science")








