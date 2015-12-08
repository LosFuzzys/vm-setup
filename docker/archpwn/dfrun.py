#!/usr/bin/env python3

import sys
import os
import shlex
import hashlib
import json
import re
import subprocess as sp
from pwd import getpwnam


class CommandFailedError(Exception):
    pass


class DFRunner:

    DEFAULT_TIMEOUT = 60 * 5  # 5 minutes

    def __init__(self, filename):
        self.filename = filename
        self.uid = os.getuid()
        self.user = 'root'
        self.workdir = '/'
        self.env = {}
        self.lines = []
        self.executed = []
        with open(self.filename) as f:
            self.lines = f.read().split("\n")

    def next_line(self):
        l = self.lines[0]
        del self.lines[0]
        return l

    def execute(self, args):
        if isinstance(args, str):
            args = shlex.split(args)

        uid = getpwnam(self.user).pw_uid
        os.seteuid(uid)
        env = os.environ.copy()
        for k, v in self.env:
            env[k] = v
        try:
            p = sp.Popen(args, shell=True, stderr=sp.PIPE, env=env)
            out, err = p.communicate(timeout=DFRunner.DEFAULT_TIMEOUT)
        except sp.TimeoutExpired:
            p.kill()
            out, err = p.communicate()
        os.seteuid(self.uid)

        if p.returncode != 0 or err:
            s = "Command '{}' failed with returncode {}"\
                .format(args, p.returncode)
            print(s, file=sys.stderr)
            print(err, file=sys.stderr)
            raise CommandFailedError(s)

    def set_env(self, args):
        name, val = args.split(" ", 1)
        if "$" in val:
            m = re.search("\$[0-9A-Za-z]+")
            while m:
                k = m.group().replace("$", "")
                val = val.replace(m.group(), os.getenv(k))
                m = re.search("\$[0-9A-Za-z]+")
        self.env[name] = val

    def step(self):
        line = self.next_line()
        cmd, args = line.split(" ", 1)
        cmd = cmd.upper()

        h = hashlib.sha256()
        h.update(cmd)
        h.update(args)
        lineid = h.hexdigest()

        if cmd == "USER":
            self.user = args
        elif cmd == "WORKDIR":
            self.workdir = args
        elif cmd == "RUN":
            self.execute(args)
        elif cmd == "CMD":
            self.execute(json.loads(args))
        elif cmd == "ENV":
            self.set_env(args)
        else:
            print("Unsupported command:", cmd, file=sys.stderr)
            print("'" + line + "'")

        self.executed.append(lineid)

    def run_all(self):
        pass
