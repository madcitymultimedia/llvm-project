# TestSwiftRegex.py
#
# This source file is part of the Swift.org open source project
#
# Copyright (c) 2014 - 2016 Apple Inc. and the Swift project authors
# Licensed under Apache License v2.0 with Runtime Library Exception
#
# See https://swift.org/LICENSE.txt for license information
# See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
#
# ------------------------------------------------------------------------------
"""
Test Swift's regex support
"""
import lldb
from lldbsuite.test.lldbtest import *
from lldbsuite.test.decorators import *
import lldbsuite.test.lldbutil as lldbutil


class TestSwiftRegex(TestBase):
    mydir = TestBase.compute_mydir(__file__)

    def setUp(self):
        TestBase.setUp(self)
        self.main_source = "main.swift"
        self.main_source_spec = lldb.SBFileSpec(self.main_source)

    @swiftTest
    def test_swift_regex(self):
        """Test Swift's regex support"""
        self.build()
        lldbutil.run_to_source_breakpoint(
            self, 'Set breakpoint here', self.main_source_spec)
        self.expect('v regex',
                    substrs=['_StringProcessing.Regex<(Substring, Substring, Substring, Substring)>) regex = {'])
        self.expect('po regex',
                    substrs=['Regex<(Substring, Substring, Substring, Substring)>'])

        self.expect('v dslRegex',
                    substrs=['(_StringProcessing.Regex<Substring>) dslRegex = {'])
        self.expect('po dslRegex',
                    substrs=['Regex<Substring>'])

    @swiftTest
    @skipIf(macos_version=["<", "13"])
    def test_swift_regex_in_exp(self):
        """Test Swift's regex support"""
        self.build()
        lldbutil.run_to_source_breakpoint(
            self, 'Set breakpoint here', self.main_source_spec)

        # Make sure we can use the extended syntax without enabling anything.
        self.expect('e -- #/Order from <(.*)>, type: (.*), count in dozen: ([0-9]+)/#',
                    substrs=['_StringProcessing.Regex<(Substring, Substring, Substring, Substring)>'])

        self.runCmd(
            "settings set target.experimental.swift-enable-bare-slash-regex true")
        self.expect('e -- /Order from <(.*)>, type: (.*), count in dozen: ([0-9]+)/',
                    substrs=['_StringProcessing.Regex<(Substring, Substring, Substring, Substring)>'])
