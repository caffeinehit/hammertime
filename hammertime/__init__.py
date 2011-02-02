import os
import sys
import git
import optparse
import simplejson
from datetime import datetime

VERSION = (0,0,1)

usage = """git time [options]
   or: git time start [options]
   or: git time stop [options]
   or: git time show [options]
"""

parser = optparse.OptionParser(usage)

parser.add_option('-b','--branch', action='store', dest='branch',
        default='git-time',
        help = 'Sets the name of the branch that saves timing data.')

parser.add_option('-d','--dir', action='store', dest='folder',
        default='.git-time', 
        help='Sets the folder that data is saved in.')

parser.add_option('-f','--file', action='store', dest='file',
        default='times.json', help='Sets the file that data is saved in.')

parser.add_option('-i','--indent', action='store', dest='indent', default=None,
        help='Add indentation to JSON output, eg: -i 4')

parser.add_option('-m','--message',action='store', dest='message',
        default=False, help='Optional message with the start/stop commands')

opts, args = parser.parse_args()

try:
    opts.indent = int(opts.indent)
except TypeError:
    opts.indent = None

DIR = os.getcwd()
FOLDER = os.path.join(DIR, opts.folder)
FILE = os.path.join(FOLDER, opts.file)

try:
    cmd = args[0]
except IndexError:
    cmd = 'default'


class DatetimeEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super(DatetimeEncoder, self).default(o)

def datetime_hook(obj):
    try:
        if obj.get('time', False):
            obj['time'] = datetime.strptime(obj.get('time'), '%Y-%m-%dT%H:%M:%S.%f')
    finally:
        return obj

serialize_delta = lambda delta: str(delta).split('.')[0] # No need for miliseconds

class Timer(dict):
    def start(self, opts):
        self['times'].append({
            'start': {
                'time': datetime.now(),
                'message': opts.message or None
            }
        })

    def stop(self, opts):
        time = self['times'][-1]

        now = datetime.now()

        time.update({
            'stop': {
                'time': now,
                'message': opts.message or None
            }
        })

        if time['start']['time']:
            delta = now - time['start']['time'] 
            time['delta'] = serialize_delta(delta)
        else:
            time['delta'] = None



def init(repo, opts):
    # Make sure a branch is available
    if not hasattr(repo.heads, opts.branch):
        repo.git.branch(opts.branch)

    # Switch the branch
    getattr(repo.heads, opts.branch).checkout()

    # Make sure there's a folder
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)

    # And the data file
    if not os.path.exists(FILE):
        open(FILE, 'w').close()

    # Load the data
    try:
        data = simplejson.load(open(FILE),object_hook = datetime_hook)
    except simplejson.decoder.JSONDecodeError:
        data = dict(times=[])

    timer = Timer()
    timer.update(data)
    return timer


def write(repo, opts, timer):
    simplejson.dump(timer, open(FILE, 'w'), cls=DatetimeEncoder)
    repo.index.add([FILE])
    repo.index.commit('Timing')

def start(repo, opts, timer):
    timer.start(opts)

def stop(repo, opts, timer):
    timer.stop(opts)

def show(repo, opts, timer):
    print simplejson.dumps(timer, indent=opts.indent, cls=DatetimeEncoder)

def default(repo, opts, timer):
    parser.print_usage()

commands=dict(start=start, stop=stop, show=show, default=default)

def main():
    try:
        repo = git.Repo(DIR)
    except git.exc.InvalidGitRepositoryError:
        print "fatal: Not a git repository"
        sys.exit(1)

    if cmd not in commands.keys():
        parser.print_usage()
        sys.exit(1)

    try:
        # Save old branch
        branch = repo.head.reference

        # Stash current changes to not lose anything
        repo.git.stash()

        timer = init(repo, opts)
        
        commands[cmd](repo, opts, timer)

        write(repo, opts, timer)
    finally:
        # Switch back to old branch
        getattr(repo.heads, branch.name).checkout()

        # Pop the stashed changes
        try: repo.git.stash('pop')
        except: pass

if __name__ == '__main__': main()
