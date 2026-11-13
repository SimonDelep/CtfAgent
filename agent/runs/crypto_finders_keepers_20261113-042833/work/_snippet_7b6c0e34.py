import subprocess
result = subprocess.run(['python3', '-c', 'import cv2; print(cv2.__version__)'], capture_output=True, text=True)
print("OpenCV version:", result.stdout.strip(), result.stderr.strip())