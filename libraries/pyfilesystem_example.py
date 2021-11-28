from fs.osfs import OSFS

with OSFS(".") as mydir:
    if not mydir.exists("testfile"):
        print("Nope")
    else:
        print("Yes")

    with mydir.open("pendulum_example.py") as myfile:
        content = myfile.read()
        print(content)

    info = mydir.getinfo("requests_example.py", namespaces=["details"])
    print(info, info.is_dir, info.size, info.type, info.modified)


    # directory listing
    mydir.tree()

    print(mydir.listdir("."))
    print(list(mydir.scandir(".")))
    print(list(mydir.filterdir(".", files=["*.py"])))

    # walking
    for path in mydir.walk.files():
        print(path)

    for path in mydir.walk.dirs():
        print(path)
    