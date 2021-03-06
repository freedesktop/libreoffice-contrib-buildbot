#! /usr/bin/env python3
#
# This file is part of the LibreOffice project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

# vim: set et sw=4 ts=4:
import os.path
import sh
import tempfile

def createTestRepo(commitmultiplier=1):
    testdir = tempfile.mkdtemp()
    git = sh.git.bake('--no-pager',_cwd=testdir)
    git.init()
    touch = sh.touch.bake(_cwd=testdir)
    for commit in range(0,10*commitmultiplier):
        touch('commit%d' % commit)
        git.add('commit%d' % commit)
        git.commit('.', '-m', 'commit %d' % commit)
        if commit == 0:
            git.tag('pre-branchoff-1')
        elif commit == 3*commitmultiplier:
            git.tag('pre-branchoff-2')
        elif commit== 5*commitmultiplier:
            git.tag('branchpoint')
        elif commit == 7*commitmultiplier:
            git.tag('post-branchoff-1')
        elif commit == 9*commitmultiplier:
            git.tag('post-branchoff-2')
    git.checkout('-b', 'branch', 'branchpoint')
    for commit in range(commitmultiplier,10*commitmultiplier):
        touch('branch%d' % commit)
        git.add('branch%d' % commit)
        git.commit('.', '-m', 'branch %d' % commit)
        if commit == 7*commitmultiplier:
            git.tag('post-branchoff-on-branch-1')
        elif commit == 9*commitmultiplier:
            git.tag('post-branchoff-on-branch-2')
    return (testdir, git)
# vim: set et sw=4 ts=4:
