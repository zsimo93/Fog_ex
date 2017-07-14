from flask import Flask, request, make_response, jsonify
import sys
from os.path import isfile, join
import os
import codecs

workdir = "/action"
proxy = Flask(__name__)

code = None
filename = None

@proxy.route("/run", methods=["POST"])
def run():
    args = request.json
    print args

    fn = compile(code, filename=filename, mode='exec')

    namespace = {}
    result = None
    try:
        namespace['param'] = args
        exec(fn, namespace)
        exec('fun = %s(param)' % "main", namespace)
        result = namespace['fun']
    except Exception, e:
                    return make_response(str(e), 502)

    if result and isinstance(result, dict):
        return make_response(jsonify(result), 200)
    else:
        return make_response('The action did not return a dictionary.', 502)


if __name__ == '__main__':
    files = os.listdir(workdir)

    path_to_virtualenv = workdir + '/virtualenv'
    if os.path.isdir(path_to_virtualenv):
        # activate the virtualenv using activate_this.py contained in the virtualenv
        activate_this_file = path_to_virtualenv + '/bin/activate_this.py'
        if os.path.exists(activate_this_file):
            with open(activate_this_file) as f:
                code = compile(f.read(), activate_this_file, 'exec')
                exec(code, dict(__file__=activate_this_file))
        else:
            sys.stderr.write('Invalid virtualenv. Zip file does not include /virtualenv/bin/' + os.path.basename(activate_this_file) + '\n')

    files = [file for file in os.listdir(workdir) if isfile(join(workdir, file)) and file.endswith(".py")]
    if len(files) == 1:
        filename = join(workdir, files[0])
        with codecs.open(filename, 'r', 'utf-8') as m:
                code = m.read()
    else:
        for f in files:
            if f == "_main_.py":
                filename = join(workdir, f)
                with codecs.open(filename, 'r', 'utf-8') as m:
                    code = m.read()
                sys.path.insert(0, workdir)
                os.chdir(workdir)
                break
    proxy.run(host="0.0.0.0", port=8080)
