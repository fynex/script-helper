# script-helper.py

This repos keeps my little script-helper.py file, which is intended to shorten the usage of some recurring code lines in python. 
The main idea is to safe time and make the calls to the functions more descriptive. An example for that is the wrapping of the function `shutil.move` to `File.mv` or `subprocess.check_output` to `System.run_get_output`.
And also shorten the multi-line file read operations to `File.read` (inspired by ruby).
