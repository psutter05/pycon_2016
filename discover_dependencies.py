import os


def get_python_files(root_path):
    cwd = os.getcwd()
    os.chdir(root_path)
    file_paths = [os.path.join(base, file_path)
                  for base, _, file_paths in os.walk('.')
                  for file_path in file_paths]
    python_files = list(filter(is_python_file, file_paths))

    os.chdir(cwd)

    return python_files


def is_python_file(file_path):
    return file_path.split('.')[-1] == 'py'


def get_deps(project, file_path):
    cwd = os.getcwd()
    os.chdir(project)

    in_deps = [file_path]
    out_deps = []

    delimiters = set("'" + '"')

    with open(file_path, 'r') as f:
        for line in f:
            params = get_params(line)
            if params[0] and delimiters & set(params[0]):
                in_deps.append(remove_quotes(params[0]))
            if params[1] and delimiters & set(params[1]):
                out_deps.append(remove_quotes(params[1]))

    os.chdir(cwd)

    return in_deps, out_deps

def remove_quotes(s):
     return s.replace('"', '').replace("'", '')

def get_params(line):
    if 'odo' in line and ')' in line and '(' in line:
        params = (line
                  .split('odo')[1]
                  .split(')')[0]
                  .split('(')[1]
                  .split(','))
        if len(params) == 2:
            return (params[0].strip(), params[1].strip())
        else:
            return (None, None)
    else:
        return (None, None)

def dep_to_drake(script, dep):
    template = "{out}<- {deps}\n  python3 {script}"
    drakes = []
    for out in dep[1]:
        drakes.append(template.format(out=out, deps=', '.join(dep[0]), script=script))

    return '\n'.join(drakes)

if __name__ == '__main__':
    project = 'test_project'

    python_files = get_python_files(project)
    deps = {f:get_deps(project, f) for f in python_files}
    drake = '\n\n'.join([dep_to_drake(script, dep) for script, dep in deps.items()])

    with open(os.path.join(project, 'drake.d'), 'w') as f:
        f.write(drake)
