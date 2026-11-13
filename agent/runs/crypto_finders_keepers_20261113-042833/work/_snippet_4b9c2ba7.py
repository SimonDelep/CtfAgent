import subprocess
result = subprocess.run(['python3', '-c', 'import moviepy; print(moviepy.__version__)'], capture_output=True, text=True)
print("MoviePy:", result.stdout.strip(), result.stderr.strip())