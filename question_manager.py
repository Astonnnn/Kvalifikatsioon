import subprocess
import platform

def generate_mcq(topic):
    prompt = f"""Generate a multiple choice question about: {topic}.
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
    print(type(result.stdout))
    print(result.stdout)
    return result.stdout

generate_mcq("Science")


