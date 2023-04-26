import subprocess
#gọi hàm echo
s = subprocess.check_output(["echo", "Hello World!"])

print(str(s))
