import subprocess

if __name__ == "__main__":
    proc = subprocess.Popen(["./example.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()
    if proc.returncode == 0:
        print(f"This is what I've got: {output}")
    else:
        print(f"There was some error: {error}")
