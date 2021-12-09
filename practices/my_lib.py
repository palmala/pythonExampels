import subprocess


def give_me_something():
    proc = subprocess.Popen(["cat", "doesntexist.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()
    if proc.returncode == 0:
        return output
    else:
        return f"ERROR: {error}"