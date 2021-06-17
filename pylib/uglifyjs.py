import shutil
import subprocess


################################################################################
# Uglify Copyfile calls an uglification process on an entire file and writes
# the output to a new file.
################################################################################
def uglify_copyfile(in_file: str, out_file: str) -> None:
    try:
        subprocess.run(["./node_modules/.bin/terser", "--mangle", "--compress", "-o", out_file, in_file])
    except Exception as e:
        print("WARNING: Javascript compression failed")
        print("        ", e)
        print("        Falling back to regular copy")
        shutil.copyfile(in_file, out_file)


################################################################################
# Uglify js String calls and uglification / minification process on a single
# string, which is then returned.
################################################################################
def uglify_js_string(js_string: str) -> str:
    try:
        result = subprocess.run(["./node_modules/.bin/terser", "--mangle", "--compress"], input=js_string.encode("utf-8"), stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8")
    except Exception as e:
        print("WARNING: Javascript compression failed")
        print("        ", e)
    return js_string
