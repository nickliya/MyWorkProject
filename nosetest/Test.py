# coding = utf-8
# author:semishigure
from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import nose


class Testclass:

    def setup(self):
        print 'start'

    def teardown(self):
        print 'stop'

    def testfunc1(self):

        print 'this is case1'

    def testfunc2(self):
        print 'this is case2'

    def testfunc3(self):
        print 'this is case3'
