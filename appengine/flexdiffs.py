
import difflib
import os


d = difflib.Differ()

for root, dirs, files in os.walk("./flexible"):
    #print(f"root={root}")
    #print(f"    dirs={dirs}")
    #print(f"        files={files}")
    print("")
    print("============================================")
    print(f"Checking folder {root}")
    print("============================================")
    print("")
    
    for name in files:
        if name in ("noxfile_config.py", "app.yaml", "README.md", "requirements.txt", "requirements-test.txt"):
            continue

        if name[-4:] in (".jpg", ".png", ".gif", ".mp4"):
            continue

        current_filename = os.path.join(root, name)
        old_filename = current_filename.replace("/flexible/", "/flexible_python37_and_earlier/")

        #print(f"Compare {current_filename} to {old_filename}")
        if not os.path.isfile(old_filename):
            print(f"**** New file {current_filename}")
            continue
        
        #print(f"Reading {current_filename}...")
        with open(current_filename, "r") as f:
            current = f.readlines()
        with open(old_filename, "r") as f:
            old = f.readlines()

        #diffs = list(d.compare(current, old))
        diffs = list(difflib.unified_diff(current, old, fromfile=current_filename, tofile=old_filename))
        if diffs:
            print(f"---- {len(diffs)} Differences for {current_filename}")
            for line in diffs:
                print(f"    {line.rstrip()}")
        else:
            print(f"~~~~ No changes for {current_filename}")
