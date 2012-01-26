import os
import sys
import git
import optparse
from datetime import datetime, timedelta

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "Error: simplejson required"
        sys.exit(1)

__version__ = "0.2.2"

usage = """git time [options]
   or: git time start [options]
   or: git time stop [options]
   or: git time show [options]
"""

parser = optparse.OptionParser(usage)

parser.add_option('-b','--branch', action='store', dest='branch',
        default='hammertime',
        help = 'Sets the name of the branch that saves timing data.')

parser.add_option('-d','--dir', action='store', dest='folder',
        default='.hammertime', 
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
FOLDER = lambda repo: os.path.join(repo.working_dir, opts.folder)
FILE = lambda repo: os.path.join(repo.working_dir, opts.folder, opts.file)

try:
    cmd = args[0]
except IndexError:
    cmd = 'default'


class DatetimeEncoder(json.JSONEncoder):
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
    if not os.path.exists(FOLDER(repo)):
        os.mkdir(FOLDER(repo))

    # And the data file
    if not os.path.exists(FILE(repo)):
        open(FILE(repo), 'w').close()

    # Load the data
    try:
        data = json.load(open(FILE(repo)),object_hook = datetime_hook)
    except ValueError:
        data = dict(times=[])

    timer = Timer()
    timer.update(data)
    return timer


def write(repo, opts, timer):
    json.dump(timer, open(FILE(repo), 'w'), cls=DatetimeEncoder)
    repo.index.add([FILE(repo)])
    repo.index.commit(opts.message or 'Hammertime!')

def start(repo, opts, timer):
    timer.start(opts)

def stop(repo, opts, timer):
    timer.stop(opts)

def total(repo, opts, timer):
    total = timedelta(seconds = 0)
    
    for time in timer['times']:
        try:
            bits = map(int, time['delta'].split(':'))
            delta = (
                timedelta(seconds = bits[0] * 3600)
                + timedelta(seconds = bits[1] * 60)
                + timedelta(seconds = bits[2])
            )
        except (KeyError, IndexError):
            delta = timedelta(seconds = 0)
    
        total += delta
    
    print total

def show(repo, opts, timer):
    print json.dumps(timer, indent=opts.indent, cls=DatetimeEncoder)

def default(repo, opts, timer):
    parser.print_usage()

commands=dict(start=start, stop=stop, show=show, default=default, total=total)

def main():
    try:
        repo = git.Repo(DIR)
    except git.exc.InvalidGitRepositoryError:
        print "fatal: Not a git repository"
        sys.exit(1)

    if cmd not in commands.keys():
        parser.print_usage()
        sys.exit(1)

    if len(repo.heads) == 0:
        print """fatal: No initial commit. 
       Perhaps create a master branch and an inital commit."""
        sys.exit(1)

    try:
        # Save old branch
        branch = repo.head.reference

        # Stash current changes to not lose anything
        repo.git.stash()

        timer = init(repo, opts)
        
        commands[cmd](repo, opts, timer)

        if cmd in ['start','stop']:
            write(repo, opts, timer)
    finally:
        # Switch back to old branch
        getattr(repo.heads, branch.name).checkout()

        # Pop the stashed changes
        try: repo.git.stash('pop')
        except: pass

if __name__ == '__main__': main()
