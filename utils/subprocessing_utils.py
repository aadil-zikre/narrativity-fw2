import subprocess
def run_command(command, return_output = False):
    with subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True, universal_newlines=True) as p:
        print(f"Running Command (first 150 chars) :: {command[:150]}")
        output = p.stdout.readlines()
        print("output :: ", ''.join(output))
        print("error :: ", p.stderr.read())
    print("return code :: ", p.returncode)
    if return_output:
            res = set(output)
            res.discard('\n')
            return list(res)
cmd = run_command