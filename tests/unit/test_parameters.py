#!/usr/bin/env
# Copyright (c) 2012 Mitch Garnaat http://garnaat.org/
# Copyright 2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
import unittest
import botocore.parameters
import botocore.exceptions


class TimestampTest(unittest.TestCase):

    def test_timestamp(self):
        p = botocore.parameters.TimestampParameter(name='foo')
        d = {}
        ts = '2012-10-12T00:00'
        p.build_parameter_query(ts, d)
        assert d['foo'] == ts
        ts = '2012-10-1200:00'
        self.assertRaises(botocore.exceptions.ValidationError,
                          p.build_parameter_query,
                          value=ts, built_params=d)

    def test_integer(self):
        p = botocore.parameters.IntegerParameter(name='foo')
        d = {}
        p.build_parameter_query('123', d)
        assert d['foo'] == '123'
        self.assertRaises(botocore.exceptions.ValidationError,
                          p.build_parameter_query,
                          value='123.4', built_params=d)

    def test_integer_range(self):
        p = botocore.parameters.IntegerParameter(name='foo', min=0, max=10)
        d = {}
        p.build_parameter_query('9', d)
        assert d['foo'] == '9'
        self.assertRaises(botocore.exceptions.ValidationError,
                          p.build_parameter_query,
                          value='8.4', built_params=d)
        self.assertRaises(botocore.exceptions.RangeError,
                          p.build_parameter_query,
                          value='100', built_params=d)

    def test_float(self):
        p = botocore.parameters.FloatParameter(name='foo')
        d = {}
        p.build_parameter_query('123.4', d)
        assert d['foo'] == '123.4'
        self.assertRaises(botocore.exceptions.ValidationError,
                          p.build_parameter_query,
                          value='true', built_params=d)

    def test_float_range(self):
        p = botocore.parameters.FloatParameter(name='foo', min=0, max=10)
        d = {}
        p.build_parameter_query('9.0', d)
        assert d['foo'] == '9.0'
        self.assertRaises(botocore.exceptions.RangeError,
                          p.build_parameter_query,
                          value='100', built_params=d)

    def test_boolean(self):
        p = botocore.parameters.BooleanParameter(name='foo')
        d = {}
        p.build_parameter_query('true', d)
        assert d['foo'] == 'true'
        p.build_parameter_query('True', d)
        assert d['foo'] == 'true'
        p.build_parameter_query('TRUE', d)
        assert d['foo'] == 'true'
        p.build_parameter_query('false', d)
        assert d['foo'] == 'false'
        p.build_parameter_query('False', d)
        assert d['foo'] == 'false'
        p.build_parameter_query('FALSE', d)
        assert d['foo'] == 'false'
        self.assertRaises(botocore.exceptions.ValidationError,
                          p.build_parameter_query,
                          value='100', built_params=d)


if __name__ == "__main__":
    unittest.main()
