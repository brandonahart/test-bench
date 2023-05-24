import subprocess

#run other script
res = subprocess.run(["python3", "blob.py", "2", "resume2", "bhart.pdf"], capture_output=True)

print(res.stdin)
print(res.stdout)
print(res.stderr)
