# Copyright (C) 2003-2005 Peter J. Verveer
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# 3. The name of the author may not be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import division, print_function, absolute_import

import math
import numpy
import numpy as np
from numpy import fft
from numpy.testing import assert_, assert_equal, assert_array_equal, \
        TestCase, run_module_suite, \
        assert_array_almost_equal, assert_almost_equal
import scipy.ndimage as ndimage

eps = 1e-12


def sumsq(a, b):
    return math.sqrt(((a - b)**2).sum())


class TestNdimage:

    def setUp(self):
        # list of numarray data types
        self.integer_types = [numpy.int8, numpy.uint8, numpy.int16,
                numpy.uint16, numpy.int32, numpy.uint32,
                numpy.int64, numpy.uint64]

        self.float_types = [numpy.float32, numpy.float64]

        self.types = self.integer_types + self.float_types

        # list of boundary modes:
        self.modes = ['nearest', 'wrap', 'reflect', 'mirror', 'constant']

    def test_correlate01(self):
        "correlation 1"
        array = numpy.array([1, 2])
        weights = numpy.array([2])
        expected = [2, 4]

        output = ndimage.correlate(array, weights)
        assert_array_almost_equal(output, expected)

        output = ndimage.convolve(array, weights)
        assert_array_almost_equal(output, expected)

        output = ndimage.correlate1d(array, weights)
        assert_array_almost_equal(output, expected)

        output = ndimage.convolve1d(array, weights)
        assert_array_almost_equal(output, expected)

    def test_correlate02(self):
        "correlation 2"
        array = numpy.array([1, 2, 3])
        kernel = numpy.array([1])

        output = ndimage.correlate(array, kernel)
        assert_array_almost_equal(array, output)

        output = ndimage.convolve(array, kernel)
        assert_array_almost_equal(array, output)

        output = ndimage.correlate1d(array, kernel)
        assert_array_almost_equal(array, output)

        output = ndimage.convolve1d(array, kernel)
        assert_array_almost_equal(array, output)

    def test_correlate03(self):
        "correlation 3"
        array = numpy.array([1])
        weights = numpy.array([1, 1])
        expected = [2]

        output = ndimage.correlate(array, weights)
        assert_array_almost_equal(output, expected)

        output = ndimage.convolve(array, weights)
        assert_array_almost_equal(output, expected)

        output = ndimage.correlate1d(array, weights)
        assert_array_almost_equal(output, expected)

        output = ndimage.convolve1d(array, weights)
        assert_array_almost_equal(output, expected)

    def test_correlate04(self):
        "correlation 4"
        array = numpy.array([1, 2])
        tcor = [2, 3]
        tcov = [3, 4]
        weights = numpy.array([1, 1])
        output = ndimage.correlate(array, weights)
        assert_array_almost_equal(output, tcor)
        output = ndimage.convolve(array, weights)
        assert_array_almost_equal(output, tcov)
        output = ndimage.correlate1d(array, weights)
        assert_array_almost_equal(output, tcor)
        output = ndimage.convolve1d(array, weights)
        assert_array_almost_equal(output, tcov)

    def test_correlate05(self):
        "correlation 5"
        array = numpy.array([1, 2, 3])
        tcor = [2, 3, 5]
        tcov = [3, 5, 6]
        kernel = numpy.array([1, 1])
        output = ndimage.correlate(array, kernel)
        assert_array_almost_equal(tcor, output)
        output = ndimage.convolve(array, kernel)
        assert_array_almost_equal(tcov, output)
        output = ndimage.correlate1d(array, kernel)
        assert_array_almost_equal(tcor, output)
        output = ndimage.convolve1d(array, kernel)
        assert_array_almost_equal(tcov, output)

    def test_correlate06(self):
        "correlation 6"
        array = numpy.array([1, 2, 3])
        tcor = [9, 14, 17]
        tcov = [7, 10, 15]
        weights = numpy.array([1, 2, 3])
        output = ndimage.correlate(array, weights)
        assert_array_almost_equal(output, tcor)
        output = ndimage.convolve(array, weights)
        assert_array_almost_equal(output, tcov)
        output = ndimage.correlate1d(array, weights)
        assert_array_almost_equal(output, tcor)
        output = ndimage.convolve1d(array, weights)
        assert_array_almost_equal(output, tcov)

    def test_correlate07(self):
        "correlation 7"
        array = numpy.array([1, 2, 3])
        expected = [5, 8, 11]
        weights = numpy.array([1, 2, 1])
        output = ndimage.correlate(array, weights)
        assert_array_almost_equal(output, expected)
        output = ndimage.convolve(array, weights)
        assert_array_almost_equal(output, expected)
        output = ndimage.correlate1d(array, weights)
        assert_array_almost_equal(output, expected)
        output = ndimage.convolve1d(array, weights)
        assert_array_almost_equal(output, expected)

    def test_correlate08(self):
        "correlation 8"
        array = numpy.array([1, 2, 3])
        tcor = [1, 2, 5]
        tcov = [3, 6, 7]
        weights = numpy.array([1, 2, -1])
        output = ndimage.correlate(array, weights)
        assert_array_almost_equal(output, tcor)
        output = ndimage.convolve(array, weights)
        assert_array_almost_equal(output, tcov)
        output = ndimage.correlate1d(array, weights)
        assert_array_almost_equal(output, tcor)
        output = ndimage.convolve1d(array, weights)
        assert_array_almost_equal(output, tcov)

    def test_correlate09(self):
        "correlation 9"
        array = []
        kernel = numpy.array([1, 1])
        output = ndimage.correlate(array, kernel)
        assert_array_almost_equal(array, output)
        output = ndimage.convolve(array, kernel)
        assert_array_almost_equal(array, output)
        output = ndimage.correlate1d(array, kernel)
        assert_array_almost_equal(array, output)
        output = ndimage.convolve1d(array, kernel)
        assert_array_almost_equal(array, output)

    def test_correlate10(self):
        "correlation 10"
        array = [[]]
        kernel = numpy.array([[1, 1]])
        output = ndimage.correlate(array, kernel)
        assert_array_almost_equal(array, output)
        output = ndimage.convolve(array, kernel)
        assert_array_almost_equal(array, output)

    def test_correlate11(self):
        "correlation 11"
        array = numpy.array([[1, 2, 3],
                                [4, 5, 6]])
        kernel = numpy.array([[1, 1],
                                 [1, 1]])
        output = ndimage.correlate(array, kernel)
        assert_array_almost_equal([[4, 6, 10], [10, 12, 16]], output)
        output = ndimage.convolve(array, kernel)
        assert_array_almost_equal([[12, 16, 18], [18, 22, 24]], output)

    def test_correlate12(self):
        "correlation 12"
        array = numpy.array([[1, 2, 3],
                                [4, 5, 6]])
        kernel = numpy.array([[1, 0],
                                 [0, 1]])
        output = ndimage.correlate(array, kernel)
        assert_array_almost_equal([[2, 3, 5], [5, 6, 8]], output)
        output = ndimage.convolve(array, kernel)
        assert_array_almost_equal([[6, 8, 9], [9, 11, 12]], output)

    def test_correlate13(self):
        "correlation 13"
        kernel = numpy.array([[1, 0],
                              [0, 1]])
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                 [4, 5, 6]], type1)
            for type2 in self.types:
                output = ndimage.correlate(array, kernel,
                                                    output=type2)
                assert_array_almost_equal([[2, 3, 5], [5, 6, 8]], output)
                assert_equal(output.dtype.type, type2)

                output = ndimage.convolve(array, kernel,
                                          output=type2)
                assert_array_almost_equal([[6, 8, 9], [9, 11, 12]], output)
                assert_equal(output.dtype.type, type2)

    def test_correlate14(self):
        "correlation 14"
        kernel = numpy.array([[1, 0],
                              [0, 1]])
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                 [4, 5, 6]], type1)
            for type2 in self.types:
                output = numpy.zeros(array.shape, type2)
                ndimage.correlate(array, kernel,
                                  output=output)
                assert_array_almost_equal([[2, 3, 5], [5, 6, 8]], output)
                assert_equal(output.dtype.type, type2)

                ndimage.convolve(array, kernel, output=output)
                assert_array_almost_equal([[6, 8, 9], [9, 11, 12]], output)
                assert_equal(output.dtype.type, type2)

    def test_correlate15(self):
        "correlation 15"
        kernel = numpy.array([[1, 0],
                              [0, 1]])
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                 [4, 5, 6]], type1)
            output = ndimage.correlate(array, kernel,
                                       output=numpy.float32)
            assert_array_almost_equal([[2, 3, 5], [5, 6, 8]], output)
            assert_equal(output.dtype.type, numpy.float32)

            output = ndimage.convolve(array, kernel,
                                      output=numpy.float32)
            assert_array_almost_equal([[6, 8, 9], [9, 11, 12]], output)
            assert_equal(output.dtype.type, numpy.float32)

    def test_correlate16(self):
        "correlation 16"
        kernel = numpy.array([[0.5, 0],
                                 [0,   0.5]])
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                    [4, 5, 6]], type1)
            output = ndimage.correlate(array, kernel,
                                                output=numpy.float32)
            assert_array_almost_equal([[1, 1.5, 2.5], [2.5, 3, 4]], output)
            assert_equal(output.dtype.type, numpy.float32)

            output = ndimage.convolve(array, kernel,
                                      output=numpy.float32)
            assert_array_almost_equal([[3, 4, 4.5], [4.5, 5.5, 6]], output)
            assert_equal(output.dtype.type, numpy.float32)

    def test_correlate17(self):
        "correlation 17"
        array = numpy.array([1, 2, 3])
        tcor = [3, 5, 6]
        tcov = [2, 3, 5]
        kernel = numpy.array([1, 1])
        output = ndimage.correlate(array, kernel, origin=-1)
        assert_array_almost_equal(tcor, output)
        output = ndimage.convolve(array, kernel, origin=-1)
        assert_array_almost_equal(tcov, output)
        output = ndimage.correlate1d(array, kernel, origin=-1)
        assert_array_almost_equal(tcor, output)
        output = ndimage.convolve1d(array, kernel, origin=-1)
        assert_array_almost_equal(tcov, output)

    def test_correlate18(self):
        "correlation 18"
        kernel = numpy.array([[1, 0],
                                 [0, 1]])
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                    [4, 5, 6]], type1)
            output = ndimage.correlate(array, kernel,
                                        output=numpy.float32,
                                        mode='nearest', origin=-1)
            assert_array_almost_equal([[6, 8, 9], [9, 11, 12]], output)
            assert_equal(output.dtype.type, numpy.float32)

            output = ndimage.convolve(array, kernel,
                                      output=numpy.float32,
                                      mode='nearest', origin=-1)
            assert_array_almost_equal([[2, 3, 5], [5, 6, 8]], output)
            assert_equal(output.dtype.type, numpy.float32)

    def test_correlate19(self):
        "correlation 19"
        kernel = numpy.array([[1, 0],
                              [0, 1]])
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                 [4, 5, 6]], type1)
            output = ndimage.correlate(array, kernel,
                                       output=numpy.float32,
                                       mode='nearest', origin=[-1, 0])
            assert_array_almost_equal([[5, 6, 8], [8, 9, 11]], output)
            assert_equal(output.dtype.type, numpy.float32)

            output = ndimage.convolve(array, kernel,
                                      output=numpy.float32,
                                      mode='nearest', origin=[-1, 0])
            assert_array_almost_equal([[3, 5, 6], [6, 8, 9]], output)
            assert_equal(output.dtype.type, numpy.float32)

    def test_correlate20(self):
        "correlation 20"
        weights = numpy.array([1, 2, 1])
        expected = [[5, 10, 15], [7, 14, 21]]
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numpy.zeros((2, 3), type2)
                ndimage.correlate1d(array, weights, axis=0,
                                    output=output)
                assert_array_almost_equal(output, expected)
                ndimage.convolve1d(array, weights, axis=0,
                                   output=output)
                assert_array_almost_equal(output, expected)

    def test_correlate21(self):
        "correlation 21"
        array = numpy.array([[1, 2, 3],
                                [2, 4, 6]])
        expected = [[5, 10, 15], [7, 14, 21]]
        weights = numpy.array([1, 2, 1])
        output = ndimage.correlate1d(array, weights, axis=0)
        assert_array_almost_equal(output, expected)
        output = ndimage.convolve1d(array, weights, axis=0)
        assert_array_almost_equal(output, expected)

    def test_correlate22(self):
        "correlation 22"
        weights = numpy.array([1, 2, 1])
        expected = [[6, 12, 18], [6, 12, 18]]
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numpy.zeros((2, 3), type2)
                ndimage.correlate1d(array, weights, axis=0,
                                            mode='wrap', output=output)
                assert_array_almost_equal(output, expected)
                ndimage.convolve1d(array, weights, axis=0,
                                            mode='wrap', output=output)
                assert_array_almost_equal(output, expected)

    def test_correlate23(self):
        "correlation 23"
        weights = numpy.array([1, 2, 1])
        expected = [[5, 10, 15], [7, 14, 21]]
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numpy.zeros((2, 3), type2)
                ndimage.correlate1d(array, weights, axis=0,
                                         mode='nearest', output=output)
                assert_array_almost_equal(output, expected)
                ndimage.convolve1d(array, weights, axis=0,
                                         mode='nearest', output=output)
                assert_array_almost_equal(output, expected)

    def test_correlate24(self):
        "correlation 24"
        weights = numpy.array([1, 2, 1])
        tcor = [[7, 14, 21], [8, 16, 24]]
        tcov = [[4, 8, 12], [5, 10, 15]]
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                    [2, 4, 6]], type1)
            for type2 in self.types:
                output = numpy.zeros((2, 3), type2)
                ndimage.correlate1d(array, weights, axis=0,
                           mode='nearest', output=output, origin=-1)
                assert_array_almost_equal(output, tcor)
                ndimage.convolve1d(array, weights, axis=0,
                           mode='nearest', output=output, origin=-1)
                assert_array_almost_equal(output, tcov)

    def test_correlate25(self):
        "correlation 25"
        weights = numpy.array([1, 2, 1])
        tcor = [[4, 8, 12], [5, 10, 15]]
        tcov = [[7, 14, 21], [8, 16, 24]]
        for type1 in self.types:
            array = numpy.array([[1, 2, 3],
                                 [2, 4, 6]], type1)
            for type2 in self.types:
                output = numpy.zeros((2, 3), type2)
                ndimage.correlate1d(array, weights, axis=0,
                             mode='nearest', output=output, origin=1)
                assert_array_almost_equal(output, tcor)
                ndimage.convolve1d(array, weights, axis=0,
                             mode='nearest', output=output, origin=1)
                assert_array_almost_equal(output, tcov)

    def test_gauss01(self):
        "gaussian filter 1"
        input = numpy.array([[1, 2, 3],
                             [2, 4, 6]], numpy.float32)
        output = ndimage.gaussian_filter(input, 0)
        assert_array_almost_equal(output, input)

    def test_gauss02(self):
        "gaussian filter 2"
        input = numpy.array([[1, 2, 3],
                             [2, 4, 6]], numpy.float32)
        output = ndimage.gaussian_filter(input, 1.0)
        assert_equal(input.dtype, output.dtype)
        assert_equal(input.shape, output.shape)

    def test_gauss03(self):
        "gaussian filter 3 - single precision data"
        input = numpy.arange(100 * 100).astype(numpy.float32)
        input.shape = (100, 100)
        output = ndimage.gaussian_filter(input, [1.0, 1.0])

        assert_equal(input.dtype, output.dtype)
        assert_equal(input.shape, output.shape)

        # input.sum() is 49995000.0.  With single precision floats, we can't
        # expect more than 8 digits of accuracy, so use decimal=0 in this test.
        assert_almost_equal(output.sum(dtype='d'), input.sum(dtype='d'), decimal=0)
        assert_(sumsq(input, output) > 1.0)

    def test_gauss04(self):
        "gaussian filter 4"
        input = numpy.arange(100 * 100).astype(numpy.float32)
        input.shape = (100, 100)
        otype = numpy.float64
        output = ndimage.gaussian_filter(input, [1.0, 1.0],
                                                            output=otype)
        assert_equal(output.dtype.type, numpy.float64)
        assert_equal(input.shape, output.shape)
        assert_(sumsq(input, output) > 1.0)

    def test_gauss05(self):
        "gaussian filter 5"
        input = numpy.arange(100 * 100).astype(numpy.float32)
        input.shape = (100, 100)
        otype = numpy.float64
        output = ndimage.gaussian_filter(input, [1.0, 1.0],
                                                 order=1, output=otype)
        assert_equal(output.dtype.type, numpy.float64)
        assert_equal(input.shape, output.shape)
        assert_(sumsq(input, output) > 1.0)

    def test_gauss06(self):
        "gaussian filter 6"
        input = numpy.arange(100 * 100).astype(numpy.float32)
        input.shape = (100, 100)
        otype = numpy.float64
        output1 = ndimage.gaussian_filter(input, [1.0, 1.0],
                                                            output=otype)
        output2 = ndimage.gaussian_filter(input, 1.0,
                                                            output=otype)
        assert_array_almost_equal(output1, output2)

    def test_prewitt01(self):
        "prewitt filter 1"
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = ndimage.correlate1d(array, [-1.0, 0.0, 1.0], 0)
            t = ndimage.correlate1d(t, [1.0, 1.0, 1.0], 1)
            output = ndimage.prewitt(array, 0)
            assert_array_almost_equal(t, output)

    def test_prewitt02(self):
        "prewitt filter 2"
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = ndimage.correlate1d(array, [-1.0, 0.0, 1.0], 0)
            t = ndimage.correlate1d(t, [1.0, 1.0, 1.0], 1)
            output = numpy.zeros(array.shape, type)
            ndimage.prewitt(array, 0, output)
            assert_array_almost_equal(t, output)

    def test_prewitt03(self):
        "prewitt filter 3"
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = ndimage.correlate1d(array, [-1.0, 0.0, 1.0], 1)
            t = ndimage.correlate1d(t, [1.0, 1.0, 1.0], 0)
            output = ndimage.prewitt(array, 1)
            assert_array_almost_equal(t, output)

    def test_prewitt04(self):
        "prewitt filter 4"
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = ndimage.prewitt(array, -1)
            output = ndimage.prewitt(array, 1)
            assert_array_almost_equal(t, output)

    def test_sobel01(self):
        "sobel filter 1"
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = ndimage.correlate1d(array, [-1.0, 0.0, 1.0], 0)
            t = ndimage.correlate1d(t, [1.0, 2.0, 1.0], 1)
            output = ndimage.sobel(array, 0)
            assert_array_almost_equal(t, output)

    def test_sobel02(self):
        "sobel filter 2"
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = ndimage.correlate1d(array, [-1.0, 0.0, 1.0], 0)
            t = ndimage.correlate1d(t, [1.0, 2.0, 1.0], 1)
            output = numpy.zeros(array.shape, type)
            ndimage.sobel(array, 0, output)
            assert_array_almost_equal(t, output)

    def test_sobel03(self):
        "sobel filter 3"
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = ndimage.correlate1d(array, [-1.0, 0.0, 1.0], 1)
            t = ndimage.correlate1d(t, [1.0, 2.0, 1.0], 0)
            output = numpy.zeros(array.shape, type)
            output = ndimage.sobel(array, 1)
            assert_array_almost_equal(t, output)

    def test_sobel04(self):
        "sobel filter 4"
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            t = ndimage.sobel(array, -1)
            output = ndimage.sobel(array, 1)
            assert_array_almost_equal(t, output)

    def test_laplace01(self):
        "laplace filter 1"
        for type in [numpy.int32, numpy.float32, numpy.float64]:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = ndimage.correlate1d(array, [1, -2, 1], 0)
            tmp2 = ndimage.correlate1d(array, [1, -2, 1], 1)
            output = ndimage.laplace(array)
            assert_array_almost_equal(tmp1 + tmp2, output)

    def test_laplace02(self):
        "laplace filter 2"
        for type in [numpy.int32, numpy.float32, numpy.float64]:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = ndimage.correlate1d(array, [1, -2, 1], 0)
            tmp2 = ndimage.correlate1d(array, [1, -2, 1], 1)
            output = numpy.zeros(array.shape, type)
            ndimage.laplace(array, output=output)
            assert_array_almost_equal(tmp1 + tmp2, output)

    def test_gaussian_laplace01(self):
        "gaussian laplace filter 1"
        for type in [numpy.int32, numpy.float32, numpy.float64]:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = ndimage.gaussian_filter(array, 1.0, [2, 0])
            tmp2 = ndimage.gaussian_filter(array, 1.0, [0, 2])
            output = ndimage.gaussian_laplace(array, 1.0)
            assert_array_almost_equal(tmp1 + tmp2, output)

    def test_gaussian_laplace02(self):
        "gaussian laplace filter 2"
        for type in [numpy.int32, numpy.float32, numpy.float64]:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = ndimage.gaussian_filter(array, 1.0, [2, 0])
            tmp2 = ndimage.gaussian_filter(array, 1.0, [0, 2])
            output = numpy.zeros(array.shape, type)
            ndimage.gaussian_laplace(array, 1.0, output)
            assert_array_almost_equal(tmp1 + tmp2, output)

    def test_generic_laplace01(self):
        "generic laplace filter 1"
        def derivative2(input, axis, output, mode, cval, a, b):
            sigma = [a, b / 2.0]
            input = numpy.asarray(input)
            order = [0] * input.ndim
            order[axis] = 2
            return ndimage.gaussian_filter(input, sigma, order,
                                           output, mode, cval)
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = numpy.zeros(array.shape, type)
            tmp = ndimage.generic_laplace(array, derivative2,
                    extra_arguments=(1.0,), extra_keywords={'b': 2.0})
            ndimage.gaussian_laplace(array, 1.0, output)
            assert_array_almost_equal(tmp, output)

    def test_gaussian_gradient_magnitude01(self):
        "gaussian gradient magnitude filter 1"
        for type in [numpy.int32, numpy.float32, numpy.float64]:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = ndimage.gaussian_filter(array, 1.0, [1, 0])
            tmp2 = ndimage.gaussian_filter(array, 1.0, [0, 1])
            output = ndimage.gaussian_gradient_magnitude(array,
                                                                       1.0)
            expected = tmp1 * tmp1 + tmp2 * tmp2
            expected = numpy.sqrt(expected).astype(type)
            assert_array_almost_equal(expected, output)

    def test_gaussian_gradient_magnitude02(self):
        "gaussian gradient magnitude filter 2"
        for type in [numpy.int32, numpy.float32, numpy.float64]:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type) * 100
            tmp1 = ndimage.gaussian_filter(array, 1.0, [1, 0])
            tmp2 = ndimage.gaussian_filter(array, 1.0, [0, 1])
            output = numpy.zeros(array.shape, type)
            ndimage.gaussian_gradient_magnitude(array, 1.0,
                                                           output)
            expected = tmp1 * tmp1 + tmp2 * tmp2
            expected = numpy.sqrt(expected).astype(type)
            assert_array_almost_equal(expected, output)

    def test_generic_gradient_magnitude01(self):
        "generic gradient magnitude 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [5, 8, 3, 7, 1],
                                [5, 6, 9, 3, 5]], numpy.float64)
        def derivative(input, axis, output, mode, cval, a, b):
            sigma = [a, b / 2.0]
            input = numpy.asarray(input)
            order = [0] * input.ndim
            order[axis] = 1
            return ndimage.gaussian_filter(input, sigma, order,
                                        output, mode, cval)
        tmp1 = ndimage.gaussian_gradient_magnitude(array, 1.0)
        tmp2 = ndimage.generic_gradient_magnitude(array,
                derivative, extra_arguments=(1.0,),
                extra_keywords={'b': 2.0})
        assert_array_almost_equal(tmp1, tmp2)

    def test_uniform01(self):
        "uniform filter 1"
        array = numpy.array([2, 4, 6])
        size = 2
        output = ndimage.uniform_filter1d(array, size,
                                                   origin=-1)
        assert_array_almost_equal([3, 5, 6], output)

    def test_uniform02(self):
        "uniform filter 2"
        array = numpy.array([1, 2, 3])
        filter_shape = [0]
        output = ndimage.uniform_filter(array, filter_shape)
        assert_array_almost_equal(array, output)

    def test_uniform03(self):
        "uniform filter 3"
        array = numpy.array([1, 2, 3])
        filter_shape = [1]
        output = ndimage.uniform_filter(array, filter_shape)
        assert_array_almost_equal(array, output)

    def test_uniform04(self):
        "uniform filter 4"
        array = numpy.array([2, 4, 6])
        filter_shape = [2]
        output = ndimage.uniform_filter(array, filter_shape)
        assert_array_almost_equal([2, 3, 5], output)

    def test_uniform05(self):
        "uniform filter 5"
        array = []
        filter_shape = [1]
        output = ndimage.uniform_filter(array, filter_shape)
        assert_array_almost_equal([], output)

    def test_uniform06(self):
        "uniform filter 6"
        filter_shape = [2, 2]
        for type1 in self.types:
            array = numpy.array([[4, 8, 12],
                                    [16, 20, 24]], type1)
            for type2 in self.types:
                output = ndimage.uniform_filter(array,
                                        filter_shape, output=type2)
                assert_array_almost_equal([[4, 6, 10], [10, 12, 16]], output)
                assert_equal(output.dtype.type, type2)

    def test_minimum_filter01(self):
        "minimum filter 1"
        array = numpy.array([1, 2, 3, 4, 5])
        filter_shape = numpy.array([2])
        output = ndimage.minimum_filter(array, filter_shape)
        assert_array_almost_equal([1, 1, 2, 3, 4], output)

    def test_minimum_filter02(self):
        "minimum filter 2"
        array = numpy.array([1, 2, 3, 4, 5])
        filter_shape = numpy.array([3])
        output = ndimage.minimum_filter(array, filter_shape)
        assert_array_almost_equal([1, 1, 2, 3, 4], output)

    def test_minimum_filter03(self):
        "minimum filter 3"
        array = numpy.array([3, 2, 5, 1, 4])
        filter_shape = numpy.array([2])
        output = ndimage.minimum_filter(array, filter_shape)
        assert_array_almost_equal([3, 2, 2, 1, 1], output)

    def test_minimum_filter04(self):
        "minimum filter 4"
        array = numpy.array([3, 2, 5, 1, 4])
        filter_shape = numpy.array([3])
        output = ndimage.minimum_filter(array, filter_shape)
        assert_array_almost_equal([2, 2, 1, 1, 1], output)

    def test_minimum_filter05(self):
        "minimum filter 5"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        filter_shape = numpy.array([2, 3])
        output = ndimage.minimum_filter(array, filter_shape)
        assert_array_almost_equal([[2, 2, 1, 1, 1],
                              [2, 2, 1, 1, 1],
                              [5, 3, 3, 1, 1]], output)

    def test_minimum_filter06(self):
        "minimum filter 6"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 1, 1], [1, 1, 1]]
        output = ndimage.minimum_filter(array,
                                                 footprint=footprint)
        assert_array_almost_equal([[2, 2, 1, 1, 1],
                              [2, 2, 1, 1, 1],
                              [5, 3, 3, 1, 1]], output)

    def test_minimum_filter07(self):
        "minimum filter 7"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.minimum_filter(array,
                                                 footprint=footprint)
        assert_array_almost_equal([[2, 2, 1, 1, 1],
                              [2, 3, 1, 3, 1],
                              [5, 5, 3, 3, 1]], output)

    def test_minimum_filter08(self):
        "minimum filter 8"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.minimum_filter(array,
                                       footprint=footprint, origin=-1)
        assert_array_almost_equal([[3, 1, 3, 1, 1],
                              [5, 3, 3, 1, 1],
                              [3, 3, 1, 1, 1]], output)

    def test_minimum_filter09(self):
        "minimum filter 9"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.minimum_filter(array,
                                  footprint=footprint, origin=[-1, 0])
        assert_array_almost_equal([[2, 3, 1, 3, 1],
                              [5, 5, 3, 3, 1],
                              [5, 3, 3, 1, 1]], output)

    def test_maximum_filter01(self):
        "maximum filter 1"
        array = numpy.array([1, 2, 3, 4, 5])
        filter_shape = numpy.array([2])
        output = ndimage.maximum_filter(array, filter_shape)
        assert_array_almost_equal([1, 2, 3, 4, 5], output)

    def test_maximum_filter02(self):
        "maximum filter 2"
        array = numpy.array([1, 2, 3, 4, 5])
        filter_shape = numpy.array([3])
        output = ndimage.maximum_filter(array, filter_shape)
        assert_array_almost_equal([2, 3, 4, 5, 5], output)

    def test_maximum_filter03(self):
        "maximum filter 3"
        array = numpy.array([3, 2, 5, 1, 4])
        filter_shape = numpy.array([2])
        output = ndimage.maximum_filter(array, filter_shape)
        assert_array_almost_equal([3, 3, 5, 5, 4], output)

    def test_maximum_filter04(self):
        "maximum filter 4"
        array = numpy.array([3, 2, 5, 1, 4])
        filter_shape = numpy.array([3])
        output = ndimage.maximum_filter(array, filter_shape)
        assert_array_almost_equal([3, 5, 5, 5, 4], output)

    def test_maximum_filter05(self):
        "maximum filter 5"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        filter_shape = numpy.array([2, 3])
        output = ndimage.maximum_filter(array, filter_shape)
        assert_array_almost_equal([[3, 5, 5, 5, 4],
                              [7, 9, 9, 9, 5],
                              [8, 9, 9, 9, 7]], output)

    def test_maximum_filter06(self):
        "maximum filter 6"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 1, 1], [1, 1, 1]]
        output = ndimage.maximum_filter(array,
                                                 footprint=footprint)
        assert_array_almost_equal([[3, 5, 5, 5, 4],
                              [7, 9, 9, 9, 5],
                              [8, 9, 9, 9, 7]], output)

    def test_maximum_filter07(self):
        "maximum filter 7"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.maximum_filter(array,
                                                 footprint=footprint)
        assert_array_almost_equal([[3, 5, 5, 5, 4],
                              [7, 7, 9, 9, 5],
                              [7, 9, 8, 9, 7]], output)

    def test_maximum_filter08(self):
        "maximum filter 8"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.maximum_filter(array,
                                      footprint=footprint, origin=-1)
        assert_array_almost_equal([[7, 9, 9, 5, 5],
                              [9, 8, 9, 7, 5],
                              [8, 8, 7, 7, 7]], output)

    def test_maximum_filter09(self):
        "maximum filter 9"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.maximum_filter(array,
                                 footprint=footprint, origin=[-1, 0])
        assert_array_almost_equal([[7, 7, 9, 9, 5],
                              [7, 9, 8, 9, 7],
                              [8, 8, 8, 7, 7]], output)

    def test_rank01(self):
        "rank filter 1"
        array = numpy.array([1, 2, 3, 4, 5])
        output = ndimage.rank_filter(array, 1, size=2)
        assert_array_almost_equal(array, output)
        output = ndimage.percentile_filter(array, 100, size=2)
        assert_array_almost_equal(array, output)
        output = ndimage.median_filter(array, 2)
        assert_array_almost_equal(array, output)

    def test_rank02(self):
        "rank filter 2"
        array = numpy.array([1, 2, 3, 4, 5])
        output = ndimage.rank_filter(array, 1, size=[3])
        assert_array_almost_equal(array, output)
        output = ndimage.percentile_filter(array, 50, size=3)
        assert_array_almost_equal(array, output)
        output = ndimage.median_filter(array, (3,))
        assert_array_almost_equal(array, output)

    def test_rank03(self):
        "rank filter 3"
        array = numpy.array([3, 2, 5, 1, 4])
        output = ndimage.rank_filter(array, 1, size=[2])
        assert_array_almost_equal([3, 3, 5, 5, 4], output)
        output = ndimage.percentile_filter(array, 100, size=2)
        assert_array_almost_equal([3, 3, 5, 5, 4], output)

    def test_rank04(self):
        "rank filter 4"
        array = numpy.array([3, 2, 5, 1, 4])
        expected = [3, 3, 2, 4, 4]
        output = ndimage.rank_filter(array, 1, size=3)
        assert_array_almost_equal(expected, output)
        output = ndimage.percentile_filter(array, 50, size=3)
        assert_array_almost_equal(expected, output)
        output = ndimage.median_filter(array, size=3)
        assert_array_almost_equal(expected, output)

    def test_rank05(self):
        "rank filter 5"
        array = numpy.array([3, 2, 5, 1, 4])
        expected = [3, 3, 2, 4, 4]
        output = ndimage.rank_filter(array, -2, size=3)
        assert_array_almost_equal(expected, output)

    def test_rank06(self):
        "rank filter 6"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [5, 8, 3, 7, 1],
                                [5, 6, 9, 3, 5]])
        expected = [[2, 2, 1, 1, 1],
                [3, 3, 2, 1, 1],
                [5, 5, 3, 3, 1]]
        output = ndimage.rank_filter(array, 1, size=[2, 3])
        assert_array_almost_equal(expected, output)
        output = ndimage.percentile_filter(array, 17,
                                                    size=(2, 3))
        assert_array_almost_equal(expected, output)

    def test_rank07(self):
        "rank filter 7"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [5, 8, 3, 7, 1],
                                [5, 6, 9, 3, 5]])
        expected = [[3, 5, 5, 5, 4],
                [5, 5, 7, 5, 4],
                [6, 8, 8, 7, 5]]
        output = ndimage.rank_filter(array, -2, size=[2, 3])
        assert_array_almost_equal(expected, output)

    def test_rank08(self):
        "median filter 8"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [5, 8, 3, 7, 1],
                                [5, 6, 9, 3, 5]])
        expected = [[3, 3, 2, 4, 4],
                [5, 5, 5, 4, 4],
                [5, 6, 7, 5, 5]]
        kernel = numpy.array([2, 3])
        output = ndimage.percentile_filter(array, 50.0,
                                                    size=(2, 3))
        assert_array_almost_equal(expected, output)
        output = ndimage.rank_filter(array, 3, size=(2, 3))
        assert_array_almost_equal(expected, output)
        output = ndimage.median_filter(array, size=(2, 3))
        assert_array_almost_equal(expected, output)

    def test_rank09(self):
        "rank filter 9"
        expected = [[3, 3, 2, 4, 4],
                [3, 5, 2, 5, 1],
                [5, 5, 8, 3, 5]]
        footprint = [[1, 0, 1], [0, 1, 0]]
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = ndimage.rank_filter(array, 1,
                                                  footprint=footprint)
            assert_array_almost_equal(expected, output)
            output = ndimage.percentile_filter(array, 35,
                                                    footprint=footprint)
            assert_array_almost_equal(expected, output)

    def test_rank10(self):
        "rank filter 10"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        expected = [[2, 2, 1, 1, 1],
                [2, 3, 1, 3, 1],
                [5, 5, 3, 3, 1]]
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.rank_filter(array, 0,
                                              footprint=footprint)
        assert_array_almost_equal(expected, output)
        output = ndimage.percentile_filter(array, 0.0,
                                                    footprint=footprint)
        assert_array_almost_equal(expected, output)

    def test_rank11(self):
        "rank filter 11"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        expected = [[3, 5, 5, 5, 4],
                [7, 7, 9, 9, 5],
                [7, 9, 8, 9, 7]]
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.rank_filter(array, -1,
                                              footprint=footprint)
        assert_array_almost_equal(expected, output)
        output = ndimage.percentile_filter(array, 100.0,
                                                    footprint=footprint)
        assert_array_almost_equal(expected, output)

    def test_rank12(self):
        "rank filter 12"
        expected = [[3, 3, 2, 4, 4],
                [3, 5, 2, 5, 1],
                [5, 5, 8, 3, 5]]
        footprint = [[1, 0, 1], [0, 1, 0]]
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = ndimage.rank_filter(array, 1,
                                                  footprint=footprint)
            assert_array_almost_equal(expected, output)
            output = ndimage.percentile_filter(array, 50.0,
                                                     footprint=footprint)
            assert_array_almost_equal(expected, output)
            output = ndimage.median_filter(array,
                                                    footprint=footprint)
            assert_array_almost_equal(expected, output)

    def test_rank13(self):
        "rank filter 13"
        expected = [[5, 2, 5, 1, 1],
                [5, 8, 3, 5, 5],
                [6, 6, 5, 5, 5]]
        footprint = [[1, 0, 1], [0, 1, 0]]
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = ndimage.rank_filter(array, 1,
                                       footprint=footprint, origin=-1)
            assert_array_almost_equal(expected, output)

    def test_rank14(self):
        "rank filter 14"
        expected = [[3, 5, 2, 5, 1],
                [5, 5, 8, 3, 5],
                [5, 6, 6, 5, 5]]
        footprint = [[1, 0, 1], [0, 1, 0]]
        for type in self.types:
            array = numpy.array([[3, 2, 5, 1, 4],
                                    [5, 8, 3, 7, 1],
                                    [5, 6, 9, 3, 5]], type)
            output = ndimage.rank_filter(array, 1,
                                  footprint=footprint, origin=[-1, 0])
            assert_array_almost_equal(expected, output)

    def test_generic_filter1d01(self):
        "generic 1d filter 1"
        weights = numpy.array([1.1, 2.2, 3.3])
        def _filter_func(input, output, fltr, total):
            fltr = fltr / total
            for ii in range(input.shape[0] - 2):
                output[ii] = input[ii] * fltr[0]
                output[ii] += input[ii + 1] * fltr[1]
                output[ii] += input[ii + 2] * fltr[2]
        for type in self.types:
            a = numpy.arange(12, dtype=type)
            a.shape = (3,4)
            r1 = ndimage.correlate1d(a, weights / weights.sum(), 0,
                                              origin=-1)
            r2 = ndimage.generic_filter1d(a, _filter_func, 3,
                      axis=0, origin=-1, extra_arguments=(weights,),
                      extra_keywords={'total': weights.sum()})
            assert_array_almost_equal(r1, r2)

    def test_generic_filter01(self):
        "generic filter 1"
        filter_ = numpy.array([[1.0, 2.0], [3.0, 4.0]])
        footprint = numpy.array([[1, 0], [0, 1]])
        cf = numpy.array([1., 4.])
        def _filter_func(buffer, weights, total=1.0):
            weights = cf / total
            return (buffer * weights).sum()
        for type in self.types:
            a = numpy.arange(12, dtype=type)
            a.shape = (3,4)
            r1 = ndimage.correlate(a, filter_ * footprint)
            if type in self.float_types:
                r1 /= 5
            else:
                r1 //= 5
            r2 = ndimage.generic_filter(a, _filter_func,
                            footprint=footprint, extra_arguments=(cf,),
                            extra_keywords={'total': cf.sum()})
            assert_array_almost_equal(r1, r2)

    def test_extend01(self):
        "line extension 1"
        array = numpy.array([1, 2, 3])
        weights = numpy.array([1, 0])
        expected_values = [[1, 1, 2],
                       [3, 1, 2],
                       [1, 1, 2],
                       [2, 1, 2],
                       [0, 1, 2]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate1d(array, weights, 0,
                                         mode=mode, cval=0)
            assert_array_equal(output,expected_value)

    def test_extend02(self):
        "line extension 2"
        array = numpy.array([1, 2, 3])
        weights = numpy.array([1, 0, 0, 0, 0, 0, 0, 0])
        expected_values = [[1, 1, 1],
                       [3, 1, 2],
                       [3, 3, 2],
                       [1, 2, 3],
                       [0, 0, 0]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate1d(array, weights, 0,
                                         mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_extend03(self):
        "line extension 3"
        array = numpy.array([1, 2, 3])
        weights = numpy.array([0, 0, 1])
        expected_values = [[2, 3, 3],
                       [2, 3, 1],
                       [2, 3, 3],
                       [2, 3, 2],
                       [2, 3, 0]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate1d(array, weights, 0,
                                         mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_extend04(self):
        "line extension 4"
        array = numpy.array([1, 2, 3])
        weights = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
        expected_values = [[3, 3, 3],
                       [2, 3, 1],
                       [2, 1, 1],
                       [1, 2, 3],
                       [0, 0, 0]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate1d(array, weights, 0,
                                         mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_extend05(self):
        "line extension 5"
        array = numpy.array([[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])
        weights = numpy.array([[1, 0], [0, 0]])
        expected_values = [[[1, 1, 2], [1, 1, 2], [4, 4, 5]],
                       [[9, 7, 8], [3, 1, 2], [6, 4, 5]],
                       [[1, 1, 2], [1, 1, 2], [4, 4, 5]],
                       [[5, 4, 5], [2, 1, 2], [5, 4, 5]],
                       [[0, 0, 0], [0, 1, 2], [0, 4, 5]]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate(array, weights,
                                       mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_extend06(self):
        "line extension 6"
        array = numpy.array([[1, 2, 3],
                                [4, 5, 6],
                                [7, 8, 9]])
        weights = numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
        expected_values = [[[5, 6, 6], [8, 9, 9], [8, 9, 9]],
                       [[5, 6, 4], [8, 9, 7], [2, 3, 1]],
                       [[5, 6, 6], [8, 9, 9], [8, 9, 9]],
                       [[5, 6, 5], [8, 9, 8], [5, 6, 5]],
                       [[5, 6, 0], [8, 9, 0], [0, 0, 0]]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate(array, weights,
                                       mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_extend07(self):
        "line extension 7"
        array = numpy.array([1, 2, 3])
        weights = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
        expected_values = [[3, 3, 3],
                       [2, 3, 1],
                       [2, 1, 1],
                       [1, 2, 3],
                       [0, 0, 0]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate(array, weights,
                                                 mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_extend08(self):
        "line extension 8"
        array = numpy.array([[1], [2], [3]])
        weights = numpy.array([[0], [0], [0], [0], [0], [0], [0],
                                  [0], [1]])
        expected_values = [[[3], [3], [3]],
                       [[2], [3], [1]],
                       [[2], [1], [1]],
                       [[1], [2], [3]],
                       [[0], [0], [0]]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate(array, weights,
                                                 mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_extend09(self):
        "line extension 9"
        array = numpy.array([1, 2, 3])
        weights = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
        expected_values = [[3, 3, 3],
                       [2, 3, 1],
                       [2, 1, 1],
                       [1, 2, 3],
                       [0, 0, 0]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate(array, weights,
                                       mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_extend10(self):
        "line extension 10"
        array = numpy.array([[1], [2], [3]])
        weights = numpy.array([[0], [0], [0], [0], [0], [0], [0],
                                  [0], [1]])
        expected_values = [[[3], [3], [3]],
                       [[2], [3], [1]],
                       [[2], [1], [1]],
                       [[1], [2], [3]],
                       [[0], [0], [0]]]
        for mode, expected_value in zip(self.modes, expected_values):
            output = ndimage.correlate(array, weights,
                                       mode=mode, cval=0)
            assert_array_equal(output, expected_value)

    def test_boundaries(self):
        "boundary modes"
        def shift(x):
            return (x[0] + 0.5,)

        data = numpy.array([1,2,3,4.])
        expected = {'constant': [1.5,2.5,3.5,-1,-1,-1,-1],
                    'wrap': [1.5,2.5,3.5,1.5,2.5,3.5,1.5],
                    'mirror' : [1.5,2.5,3.5,3.5,2.5,1.5,1.5],
                    'nearest' : [1.5,2.5,3.5,4,4,4,4]}

        for mode in expected:
            assert_array_equal(expected[mode],
                               ndimage.geometric_transform(data,shift,
                                                           cval=-1,mode=mode,
                                                           output_shape=(7,),
                                                           order=1))

    def test_boundaries2(self):
        "boundary modes 2"
        def shift(x):
            return (x[0] - 0.9,)

        data = numpy.array([1,2,3,4])
        expected = {'constant': [-1,1,2,3],
                    'wrap': [3,1,2,3],
                    'mirror' : [2,1,2,3],
                    'nearest' : [1,1,2,3]}

        for mode in expected:
            assert_array_equal(expected[mode],
                               ndimage.geometric_transform(data,shift,
                                                           cval=-1,mode=mode,
                                                           output_shape=(4,)))

    def test_fourier_gaussian_real01(self):
        "gaussian fourier filter for real transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numpy.float32, numpy.float64]:
                a = numpy.zeros(shape, type)
                a[0, 0] = 1.0
                a = fft.rfft(a, shape[0], 0)
                a = fft.fft(a, shape[1], 1)
                a = ndimage.fourier_gaussian(a, [5.0, 2.5],
                                                       shape[0], 0)
                a = fft.ifft(a, shape[1], 1)
                a = fft.irfft(a, shape[0], 0)
                assert_almost_equal(ndimage.sum(a), 1)

    def test_fourier_gaussian_complex01(self):
        "gaussian fourier filter for complex transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numpy.complex64, numpy.complex128]:
                a = numpy.zeros(shape, type)
                a[0, 0] = 1.0
                a = fft.fft(a, shape[0], 0)
                a = fft.fft(a, shape[1], 1)
                a = ndimage.fourier_gaussian(a, [5.0, 2.5], -1,
                                                       0)
                a = fft.ifft(a, shape[1], 1)
                a = fft.ifft(a, shape[0], 0)
                assert_almost_equal(ndimage.sum(a.real), 1.0)

    def test_fourier_uniform_real01(self):
        "uniform fourier filter for real transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numpy.float32, numpy.float64]:
                a = numpy.zeros(shape, type)
                a[0, 0] = 1.0
                a = fft.rfft(a, shape[0], 0)
                a = fft.fft(a, shape[1], 1)
                a = ndimage.fourier_uniform(a, [5.0, 2.5],
                                                      shape[0], 0)
                a = fft.ifft(a, shape[1], 1)
                a = fft.irfft(a, shape[0], 0)
                assert_almost_equal(ndimage.sum(a), 1.0)

    def test_fourier_uniform_complex01(self):
        "uniform fourier filter for complex transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numpy.complex64, numpy.complex128]:
                a = numpy.zeros(shape, type)
                a[0, 0] = 1.0
                a = fft.fft(a, shape[0], 0)
                a = fft.fft(a, shape[1], 1)
                a = ndimage.fourier_uniform(a, [5.0, 2.5], -1, 0)
                a = fft.ifft(a, shape[1], 1)
                a = fft.ifft(a, shape[0], 0)
                assert_almost_equal(ndimage.sum(a.real), 1.0)

    def test_fourier_shift_real01(self):
        "shift filter for real transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for dtype in [numpy.float32, numpy.float64]:
                expected = numpy.arange(shape[0] * shape[1], dtype=dtype)
                expected.shape = shape
                a = fft.rfft(expected, shape[0], 0)
                a = fft.fft(a, shape[1], 1)
                a = ndimage.fourier_shift(a, [1, 1], shape[0], 0)
                a = fft.ifft(a, shape[1], 1)
                a = fft.irfft(a, shape[0], 0)
                assert_array_almost_equal(a[1:, 1:], expected[:-1, :-1])
                assert_array_almost_equal(a.imag, numpy.zeros(shape))

    def test_fourier_shift_complex01(self):
        "shift filter for complex transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numpy.complex64, numpy.complex128]:
                expected = numpy.arange(shape[0] * shape[1],
                                       dtype=type)
                expected.shape = shape
                a = fft.fft(expected, shape[0], 0)
                a = fft.fft(a, shape[1], 1)
                a = ndimage.fourier_shift(a, [1, 1], -1, 0)
                a = fft.ifft(a, shape[1], 1)
                a = fft.ifft(a, shape[0], 0)
                assert_array_almost_equal(a.real[1:, 1:], expected[:-1, :-1])
                assert_array_almost_equal(a.imag, numpy.zeros(shape))

    def test_fourier_ellipsoid_real01(self):
        "ellipsoid fourier filter for real transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numpy.float32, numpy.float64]:
                a = numpy.zeros(shape, type)
                a[0, 0] = 1.0
                a = fft.rfft(a, shape[0], 0)
                a = fft.fft(a, shape[1], 1)
                a = ndimage.fourier_ellipsoid(a, [5.0, 2.5],
                                              shape[0], 0)
                a = fft.ifft(a, shape[1], 1)
                a = fft.irfft(a, shape[0], 0)
                assert_almost_equal(ndimage.sum(a), 1.0)

    def test_fourier_ellipsoid_complex01(self):
        "ellipsoid fourier filter for complex transforms 1"
        for shape in [(32, 16), (31, 15)]:
            for type in [numpy.complex64, numpy.complex128]:
                a = numpy.zeros(shape, type)
                a[0, 0] = 1.0
                a = fft.fft(a, shape[0], 0)
                a = fft.fft(a, shape[1], 1)
                a = ndimage.fourier_ellipsoid(a, [5.0, 2.5], -1,
                                                        0)
                a = fft.ifft(a, shape[1], 1)
                a = fft.ifft(a, shape[0], 0)
                assert_almost_equal(ndimage.sum(a.real), 1.0)

    def test_spline01(self):
        "spline filter 1"
        for type in self.types:
            data = numpy.ones([], type)
            for order in range(2, 6):
                out = ndimage.spline_filter(data, order=order)
                assert_array_almost_equal(out, 1)

    def test_spline02(self):
        "spline filter 2"
        for type in self.types:
            data = numpy.array([1])
            for order in range(2, 6):
                out = ndimage.spline_filter(data, order=order)
                assert_array_almost_equal(out, [1])

    def test_spline03(self):
        "spline filter 3"
        for type in self.types:
            data = numpy.ones([], type)
            for order in range(2, 6):
                out = ndimage.spline_filter(data, order,
                                            output=type)
                assert_array_almost_equal(out, 1)

    def test_spline04(self):
        "spline filter 4"
        for type in self.types:
            data = numpy.ones([4], type)
            for order in range(2, 6):
                out = ndimage.spline_filter(data, order)
                assert_array_almost_equal(out, [1, 1, 1, 1])

    def test_spline05(self):
        "spline filter 5"
        for type in self.types:
            data = numpy.ones([4, 4], type)
            for order in range(2, 6):
                out = ndimage.spline_filter(data, order=order)
                assert_array_almost_equal(out, [[1, 1, 1, 1],
                                           [1, 1, 1, 1],
                                           [1, 1, 1, 1],
                                           [1, 1, 1, 1]])

    def test_geometric_transform01(self):
        "geometric transform 1"
        data = numpy.array([1])
        def mapping(x):
            return x
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                        data.shape,
                                                        order=order)
            assert_array_almost_equal(out, [1])

    def test_geometric_transform02(self):
        "geometric transform 2"
        data = numpy.ones([4])
        def mapping(x):
            return x
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                  data.shape, order=order)
            assert_array_almost_equal(out, [1, 1, 1, 1])

    def test_geometric_transform03(self):
        "geometric transform 3"
        data = numpy.ones([4])
        def mapping(x):
            return (x[0] - 1,)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            assert_array_almost_equal(out, [0, 1, 1, 1])

    def test_geometric_transform04(self):
        "geometric transform 4"
        data = numpy.array([4, 1, 3, 2])
        def mapping(x):
            return (x[0] - 1,)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            assert_array_almost_equal(out, [0, 4, 1, 3])

    def test_geometric_transform05(self):
        "geometric transform 5"
        data = numpy.array([[1, 1, 1, 1],
                               [1, 1, 1, 1],
                               [1, 1, 1, 1]])
        def mapping(x):
            return (x[0], x[1] - 1)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            assert_array_almost_equal(out, [[0, 1, 1, 1],
                                       [0, 1, 1, 1],
                                       [0, 1, 1, 1]])

    def test_geometric_transform06(self):
        "geometric transform 6"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        def mapping(x):
            return (x[0], x[1] - 1)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            assert_array_almost_equal(out, [[0, 4, 1, 3],
                                       [0, 7, 6, 8],
                                       [0, 3, 5, 3]])

    def test_geometric_transform07(self):
        "geometric transform 7"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        def mapping(x):
            return (x[0] - 1, x[1])
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [4, 1, 3, 2],
                                       [7, 6, 8, 5]])

    def test_geometric_transform08(self):
        "geometric transform 8"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        def mapping(x):
            return (x[0] - 1, x[1] - 1)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                   data.shape, order=order)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]])

    def test_geometric_transform10(self):
        "geometric transform 10"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        def mapping(x):
            return (x[0] - 1, x[1] - 1)
        for order in range(0, 6):
            if (order > 1):
                filtered = ndimage.spline_filter(data,
                                                           order=order)
            else:
                filtered = data
            out = ndimage.geometric_transform(filtered, mapping,
                               data.shape, order=order, prefilter=False)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]])

    def test_geometric_transform13(self):
        "geometric transform 13"
        data = numpy.ones([2], numpy.float64)
        def mapping(x):
            return (x[0] // 2,)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                        [4], order=order)
            assert_array_almost_equal(out, [1, 1, 1, 1])

    def test_geometric_transform14(self):
        "geometric transform 14"
        data = [1, 5, 2, 6, 3, 7, 4, 4]
        def mapping(x):
            return (2 * x[0],)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                        [4], order=order)
            assert_array_almost_equal(out, [1, 2, 3, 4])

    def test_geometric_transform15(self):
        "geometric transform 15"
        data = [1, 2, 3, 4]
        def mapping(x):
            return (x[0] / 2,)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                        [8], order=order)
            assert_array_almost_equal(out[::2], [1, 2, 3, 4])

    def test_geometric_transform16(self):
        "geometric transform 16"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9.0, 10, 11, 12]]
        def mapping(x):
            return (x[0], x[1] * 2)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                       (3, 2), order=order)
            assert_array_almost_equal(out, [[1, 3], [5, 7], [9, 11]])

    def test_geometric_transform17(self):
        "geometric transform 17"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0] * 2, x[1])
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                       (1, 4), order=order)
            assert_array_almost_equal(out, [[1, 2, 3, 4]])

    def test_geometric_transform18(self):
        "geometric transform 18"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0] * 2, x[1] * 2)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                       (1, 2), order=order)
            assert_array_almost_equal(out, [[1, 3]])

    def test_geometric_transform19(self):
        "geometric transform 19"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0], x[1] / 2)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                       (3, 8), order=order)
            assert_array_almost_equal(out[..., ::2], data)

    def test_geometric_transform20(self):
        "geometric transform 20"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0] / 2, x[1])
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                       (6, 4), order=order)
            assert_array_almost_equal(out[::2, ...], data)

    def test_geometric_transform21(self):
        "geometric transform 21"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (x[0] / 2, x[1] / 2)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                      (6, 8), order=order)
            assert_array_almost_equal(out[::2, ::2], data)

    def test_geometric_transform22(self):
        "geometric transform 22"
        data = numpy.array([[1, 2, 3, 4],
                               [5, 6, 7, 8],
                               [9, 10, 11, 12]], numpy.float64)
        def mapping1(x):
            return (x[0] / 2, x[1] / 2)
        def mapping2(x):
            return (x[0] * 2, x[1] * 2)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping1,
                                              (6, 8),  order=order)
            out = ndimage.geometric_transform(out, mapping2,
                                              (3, 4), order=order)
            assert_array_almost_equal(out, data)

    def test_geometric_transform23(self):
        "geometric transform 23"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x):
            return (1, x[0] * 2)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                                        (2,), order=order)
            out = out.astype(numpy.int32)
            assert_array_almost_equal(out, [5, 7])

    def test_geometric_transform24(self):
        "geometric transform 24"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        def mapping(x, a, b):
            return (a, x[0] * b)
        for order in range(0, 6):
            out = ndimage.geometric_transform(data, mapping,
                                (2,), order=order, extra_arguments=(1,),
                                extra_keywords={'b': 2})
            assert_array_almost_equal(out, [5, 7])

    def test_map_coordinates01(self):
        "map coordinates 1"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        idx = numpy.indices(data.shape)
        idx -= 1
        for order in range(0, 6):
            out = ndimage.map_coordinates(data, idx, order=order)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]])

    def test_map_coordinates02(self):
        "map coordinates 2"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        idx = numpy.indices(data.shape, numpy.float64)
        idx -= 0.5
        for order in range(0, 6):
            out1 = ndimage.shift(data, 0.5, order=order)
            out2 = ndimage.map_coordinates(data, idx,
                                                     order=order)
            assert_array_almost_equal(out1, out2)

    def test_affine_transform01(self):
        "affine_transform 1"
        data = numpy.array([1])
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1]],
                                                     order=order)
            assert_array_almost_equal(out, [1])

    def test_affine_transform02(self):
        "affine transform 2"
        data = numpy.ones([4])
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1]],
                                                     order=order)
            assert_array_almost_equal(out, [1, 1, 1, 1])

    def test_affine_transform03(self):
        "affine transform 3"
        data = numpy.ones([4])
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1]], -1,
                                                     order=order)
            assert_array_almost_equal(out, [0, 1, 1, 1])

    def test_affine_transform04(self):
        "affine transform 4"
        data = numpy.array([4, 1, 3, 2])
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1]], -1,
                                                     order=order)
            assert_array_almost_equal(out, [0, 4, 1, 3])

    def test_affine_transform05(self):
        "affine transform 5"
        data = numpy.array([[1, 1, 1, 1],
                               [1, 1, 1, 1],
                               [1, 1, 1, 1]])
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1, 0],
                                                            [0, 1]],
                                                     [0, -1], order=order)
            assert_array_almost_equal(out, [[0, 1, 1, 1],
                                       [0, 1, 1, 1],
                                       [0, 1, 1, 1]])

    def test_affine_transform06(self):
        "affine transform 6"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1, 0],
                                                            [0, 1]],
                                                     [0, -1], order=order)
            assert_array_almost_equal(out, [[0, 4, 1, 3],
                                       [0, 7, 6, 8],
                                       [0, 3, 5, 3]])

    def test_affine_transform07(self):
        "affine transform 7"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1, 0],
                                                            [0, 1]],
                                                     [-1, 0], order=order)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [4, 1, 3, 2],
                                       [7, 6, 8, 5]])

    def test_affine_transform08(self):
        "affine transform 8"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1, 0],
                                                            [0, 1]],
                                                     [-1, -1], order=order)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]])

    def test_affine_transform09(self):
        "affine transform 9"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            if (order > 1):
                filtered = ndimage.spline_filter(data,
                                                           order=order)
            else:
                filtered = data
            out = ndimage.affine_transform(filtered,[[1, 0],
                                                               [0, 1]],
                                  [-1, -1], order=order, prefilter=False)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]])

    def test_affine_transform10(self):
        "affine transform 10"
        data = numpy.ones([2], numpy.float64)
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[0.5]],
                                          output_shape=(4,), order=order)
            assert_array_almost_equal(out, [1, 1, 1, 0])

    def test_affine_transform11(self):
        "affine transform 11"
        data = [1, 5, 2, 6, 3, 7, 4, 4]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[2]], 0, (4,),
                                                     order=order)
            assert_array_almost_equal(out, [1, 2, 3, 4])

    def test_affine_transform12(self):
        "affine transform 12"
        data = [1, 2, 3, 4]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[0.5]], 0,
                                                     (8,), order=order)
            assert_array_almost_equal(out[::2], [1, 2, 3, 4])

    def test_affine_transform13(self):
        "affine transform 13"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9.0, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1, 0],
                                                            [0, 2]], 0,
                                                     (3, 2), order=order)
            assert_array_almost_equal(out, [[1, 3], [5, 7], [9, 11]])

    def test_affine_transform14(self):
        "affine transform 14"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[2, 0],
                                                            [0, 1]], 0,
                                                     (1, 4), order=order)
            assert_array_almost_equal(out, [[1, 2, 3, 4]])

    def test_affine_transform15(self):
        "affine transform 15"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[2, 0],
                                                            [0, 2]], 0,
                                                     (1, 2), order=order)
            assert_array_almost_equal(out, [[1, 3]])

    def test_affine_transform16(self):
        "affine transform 16"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[1, 0.0],
                                                            [0, 0.5]], 0,
                                                     (3, 8), order=order)
            assert_array_almost_equal(out[..., ::2], data)

    def test_affine_transform17(self):
        "affine transform 17"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[0.5, 0],
                                                            [0,   1]], 0,
                                                     (6, 4), order=order)
            assert_array_almost_equal(out[::2, ...], data)

    def test_affine_transform18(self):
        "affine transform 18"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data,
                                                     [[0.5, 0],
                                                      [0, 0.5]], 0,
                                                     (6, 8), order=order)
            assert_array_almost_equal(out[::2, ::2], data)

    def test_affine_transform19(self):
        "affine transform 19"
        data = numpy.array([[1, 2, 3, 4],
                               [5, 6, 7, 8],
                               [9, 10, 11, 12]], numpy.float64)
        for order in range(0, 6):
            out = ndimage.affine_transform(data,
                                                     [[0.5, 0],
                                                      [0, 0.5]], 0,
                                                     (6, 8), order=order)
            out = ndimage.affine_transform(out,
                                                     [[2.0, 0],
                                                      [0, 2.0]], 0,
                                                     (3, 4), order=order)
            assert_array_almost_equal(out, data)

    def test_affine_transform20(self):
        "affine transform 20"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[0], [2]], 0,
                                                     (2,), order=order)
            assert_array_almost_equal(out, [1, 3])

    def test_affine_transform21(self):
        "affine transform 21"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [[2], [0]], 0,
                                                     (2,), order=order)
            assert_array_almost_equal(out, [1, 9])

    def test_shift01(self):
        "shift 1"
        data = numpy.array([1])
        for order in range(0, 6):
            out = ndimage.shift(data, [1], order=order)
            assert_array_almost_equal(out, [0])

    def test_shift02(self):
        "shift 2"
        data = numpy.ones([4])
        for order in range(0, 6):
            out = ndimage.shift(data, [1], order=order)
            assert_array_almost_equal(out, [0, 1, 1, 1])

    def test_shift03(self):
        "shift 3"
        data = numpy.ones([4])
        for order in range(0, 6):
            out = ndimage.shift(data, -1, order=order)
            assert_array_almost_equal(out, [1, 1, 1, 0])

    def test_shift04(self):
        "shift 4"
        data = numpy.array([4, 1, 3, 2])
        for order in range(0, 6):
            out = ndimage.shift(data, 1, order=order)
            assert_array_almost_equal(out, [0, 4, 1, 3])

    def test_shift05(self):
        "shift 5"
        data = numpy.array([[1, 1, 1, 1],
                               [1, 1, 1, 1],
                               [1, 1, 1, 1]])
        for order in range(0, 6):
            out = ndimage.shift(data, [0, 1], order=order)
            assert_array_almost_equal(out, [[0, 1, 1, 1],
                                       [0, 1, 1, 1],
                                       [0, 1, 1, 1]])

    def test_shift06(self):
        "shift 6"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = ndimage.shift(data, [0, 1], order=order)
            assert_array_almost_equal(out, [[0, 4, 1, 3],
                                       [0, 7, 6, 8],
                                       [0, 3, 5, 3]])

    def test_shift07(self):
        "shift 7"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = ndimage.shift(data, [1, 0], order=order)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [4, 1, 3, 2],
                                       [7, 6, 8, 5]])

    def test_shift08(self):
        "shift 8"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            out = ndimage.shift(data, [1, 1], order=order)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]])

    def test_shift09(self):
        "shift 9"
        data = numpy.array([[4, 1, 3, 2],
                               [7, 6, 8, 5],
                               [3, 5, 3, 6]])
        for order in range(0, 6):
            if (order > 1):
                filtered = ndimage.spline_filter(data,
                                                           order=order)
            else:
                filtered = data
            out = ndimage.shift(filtered, [1, 1], order=order,
                                          prefilter=False)
            assert_array_almost_equal(out, [[0, 0, 0, 0],
                                       [0, 4, 1, 3],
                                       [0, 7, 6, 8]])

    def test_zoom1(self):
        "zoom 1"
        for order in range(0,6):
            for z in [2,[2,2]]:
                arr = numpy.array(list(range(25))).reshape((5,5)).astype(float)
                arr = ndimage.zoom(arr, z, order=order)
                assert_equal(arr.shape,(10,10))
                assert_(numpy.all(arr[-1,:] != 0))
                assert_(numpy.all(arr[-1,:] >= (20 - eps)))
                assert_(numpy.all(arr[0,:] <= (5 + eps)))
                assert_(numpy.all(arr >= (0 - eps)))
                assert_(numpy.all(arr <= (24 + eps)))

    def test_zoom2(self):
        "zoom 2"
        arr = numpy.arange(12).reshape((3,4))
        out = ndimage.zoom(ndimage.zoom(arr,2),0.5)
        assert_array_equal(out,arr)

    def test_zoom3(self):
        "zoom 3"
        err = numpy.seterr(invalid='ignore')
        arr = numpy.array([[1, 2]])
        try:
            out1 = ndimage.zoom(arr, (2, 1))
            out2 = ndimage.zoom(arr, (1,2))
        finally:
            numpy.seterr(**err)

        assert_array_almost_equal(out1, numpy.array([[1, 2], [1, 2]]))
        assert_array_almost_equal(out2, numpy.array([[1, 1, 2, 2]]))

    def test_zoom_affine01(self):
        "zoom by affine transformation 1"
        data = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]]
        for order in range(0, 6):
            out = ndimage.affine_transform(data, [0.5, 0.5], 0,
                                                     (6, 8), order=order)
            assert_array_almost_equal(out[::2, ::2], data)

    def test_zoom_infinity(self):
        """Ticket #1419"""
        err = numpy.seterr(divide='ignore')

        try:
            dim = 8
            ndimage.zoom(numpy.zeros((dim, dim)), 1./dim, mode='nearest')
        finally:
            numpy.seterr(**err)

    def test_zoom_zoomfactor_one(self):
        """Ticket #1122"""
        arr = numpy.zeros((1, 5, 5))
        zoom = (1.0, 2.0, 2.0)

        err = numpy.seterr(invalid='ignore')
        try:
            out = ndimage.zoom(arr, zoom, cval=7)
        finally:
            numpy.seterr(**err)
        ref = numpy.zeros((1, 10, 10))
        assert_array_almost_equal(out, ref)

    def test_rotate01(self):
        "rotate 1"
        data = numpy.array([[0, 0, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 0, 0]], dtype=numpy.float64)
        for order in range(0, 6):
            out = ndimage.rotate(data, 0)
            assert_array_almost_equal(out, data)

    def test_rotate02(self):
        "rotate 2"
        data = numpy.array([[0, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]], dtype=numpy.float64)
        expected = numpy.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 1, 0],
                               [0, 0, 0]], dtype=numpy.float64)
        for order in range(0, 6):
            out = ndimage.rotate(data, 90)
            assert_array_almost_equal(out, expected)

    def test_rotate03(self):
        "rotate 3"
        data = numpy.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0]], dtype=numpy.float64)
        expected = numpy.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 1, 0],
                               [0, 1, 0],
                               [0, 0, 0]], dtype=numpy.float64)
        for order in range(0, 6):
            out = ndimage.rotate(data, 90)
            assert_array_almost_equal(out, expected)

    def test_rotate04(self):
        "rotate 4"
        data = numpy.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0]], dtype=numpy.float64)
        expected = numpy.array([[0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0]], dtype=numpy.float64)
        for order in range(0, 6):
            out = ndimage.rotate(data, 90, reshape=False)
            assert_array_almost_equal(out, expected)

    def test_rotate05(self):
        "rotate 5"
        data = numpy.empty((4,3,3))
        for i in range(3):
            data[:,:,i] = numpy.array([[0,0,0],
                                       [0,1,0],
                                       [0,1,0],
                                       [0,0,0]], dtype=numpy.float64)

        expected = numpy.array([[0,0,0,0],
                            [0,1,1,0],
                            [0,0,0,0]], dtype=numpy.float64)

        for order in range(0, 6):
            out = ndimage.rotate(data, 90)
            for i in range(3):
                assert_array_almost_equal(out[:,:,i], expected)

    def test_rotate06(self):
        "rotate 6"
        data = numpy.empty((3,4,3))
        for i in range(3):
            data[:,:,i] = numpy.array([[0,0,0,0],
                                       [0,1,1,0],
                                       [0,0,0,0]], dtype=numpy.float64)

        expected = numpy.array([[0,0,0],
                            [0,1,0],
                            [0,1,0],
                            [0,0,0]], dtype=numpy.float64)

        for order in range(0, 6):
            out = ndimage.rotate(data, 90)
            for i in range(3):
                assert_array_almost_equal(out[:,:,i], expected)

    def test_rotate07(self):
        "rotate 7"
        data = numpy.array([[[0, 0, 0, 0, 0],
                             [0, 1, 1, 0, 0],
                             [0, 0, 0, 0, 0]]] * 2,
                           dtype=numpy.float64)
        data = data.transpose()
        expected = numpy.array([[[0, 0, 0],
                                [0, 1, 0],
                                [0, 1, 0],
                                [0, 0, 0],
                                [0, 0, 0]]] * 2, dtype=numpy.float64)
        expected = expected.transpose([2,1,0])

        for order in range(0, 6):
            out = ndimage.rotate(data, 90, axes=(0, 1))
            assert_array_almost_equal(out, expected)

    def test_rotate08(self):
        "rotate 8"
        data = numpy.array([[[0, 0, 0, 0, 0],
                                [0, 1, 1, 0, 0],
                                [0, 0, 0, 0, 0]]] * 2,
                              dtype=numpy.float64)
        data = data.transpose()
        expected = numpy.array([[[0, 0, 1, 0, 0],
                                [0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0]]] * 2,
                              dtype=numpy.float64)
        expected = expected.transpose()
        for order in range(0, 6):
            out = ndimage.rotate(data, 90, axes=(0, 1),
                                           reshape=False)
            assert_array_almost_equal(out, expected)

    def test_watershed_ift01(self):
        "watershed_ift 1"
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numpy.uint8)
        markers = numpy.array([[-1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0]],
                                 numpy.int8)
        out = ndimage.watershed_ift(data, markers,
                                     structure=[[1,1,1],
                                                [1,1,1],
                                                [1,1,1]])
        expected = [[-1, -1, -1, -1, -1, -1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1]]
        assert_array_almost_equal(out, expected)

    def test_watershed_ift02(self):
        "watershed_ift 2"
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numpy.uint8)
        markers = numpy.array([[-1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0]],
                                 numpy.int8)
        out = ndimage.watershed_ift(data, markers)
        expected = [[-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1,  1,  1,  1, -1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1, -1,  1,  1,  1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1]]
        assert_array_almost_equal(out, expected)

    def test_watershed_ift03(self):
        "watershed_ift 3"
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numpy.uint8)
        markers = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 2, 0, 3, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, -1]],
                                 numpy.int8)
        out = ndimage.watershed_ift(data, markers)
        expected = [[-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1,  2, -1,  3, -1, -1],
                    [-1,  2,  2,  3,  3,  3, -1],
                    [-1,  2,  2,  3,  3,  3, -1],
                    [-1,  2,  2,  3,  3,  3, -1],
                    [-1, -1,  2, -1,  3, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1]]
        assert_array_almost_equal(out, expected)

    def test_watershed_ift04(self):
        "watershed_ift 4"
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numpy.uint8)
        markers = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 2, 0, 3, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, -1]],
                              numpy.int8)
        out = ndimage.watershed_ift(data, markers,
                                    structure=[[1,1,1],
                                               [1,1,1],
                                               [1,1,1]])
        expected = [[-1, -1, -1, -1, -1, -1, -1],
                    [-1,  2,  2,  3,  3,  3, -1],
                    [-1,  2,  2,  3,  3,  3, -1],
                    [-1,  2,  2,  3,  3,  3, -1],
                    [-1,  2,  2,  3,  3,  3, -1],
                    [-1,  2,  2,  3,  3,  3, -1],
                    [-1, -1, -1, -1, -1, -1, -1]]
        assert_array_almost_equal(out, expected)

    def test_watershed_ift05(self):
        "watershed_ift 5"
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0]], numpy.uint8)
        markers = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 3, 0, 2, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, -1]],
                              numpy.int8)
        out = ndimage.watershed_ift(data, markers,
                                    structure=[[1,1,1],
                                               [1,1,1],
                                               [1,1,1]])
        expected = [[-1, -1, -1, -1, -1, -1, -1],
                    [-1,  3,  3,  2,  2,  2, -1],
                    [-1,  3,  3,  2,  2,  2, -1],
                    [-1,  3,  3,  2,  2,  2, -1],
                    [-1,  3,  3,  2,  2,  2, -1],
                    [-1,  3,  3,  2,  2,  2, -1],
                    [-1, -1, -1, -1, -1, -1, -1]]
        assert_array_almost_equal(out, expected)

    def test_watershed_ift06(self):
        "watershed_ift 6"
        data = numpy.array([[0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], numpy.uint8)
        markers = numpy.array([[-1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0]],
                                 numpy.int8)
        out = ndimage.watershed_ift(data, markers,
                                              structure=[[1,1,1],
                                                         [1,1,1],
                                                         [1,1,1]])
        expected = [[-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1]]
        assert_array_almost_equal(out, expected)

    def test_watershed_ift07(self):
        "watershed_ift 7"
        shape = (7, 6)
        data = numpy.zeros(shape, dtype=numpy.uint8)
        data = data.transpose()
        data[...] = numpy.array([[0, 1, 0, 0, 0, 1, 0],
                                    [0, 1, 0, 0, 0, 1, 0],
                                    [0, 1, 0, 0, 0, 1, 0],
                                    [0, 1, 1, 1, 1, 1, 0],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0]], numpy.uint8)
        markers = numpy.array([[-1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0]],
                                 numpy.int8)
        out = numpy.zeros(shape, dtype=numpy.int16)
        out = out.transpose()
        ndimage.watershed_ift(data, markers,
                               structure=[[1,1,1],
                                          [1,1,1],
                                          [1,1,1]],
                               output=out)
        expected = [[-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1]]
        assert_array_almost_equal(out, expected)

    def test_distance_transform_bf01(self):
        "brute force distance transform 1"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = ndimage.distance_transform_bf(data, 'euclidean',
                                                return_indices=True)
        expected = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 1, 2, 4, 2, 1, 0, 0],
                    [0, 0, 1, 4, 8, 4, 1, 0, 0],
                    [0, 0, 1, 2, 4, 2, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        assert_array_almost_equal(out * out, expected)

        expected = [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 2, 2, 1, 2, 2, 2, 2],
                     [3, 3, 3, 2, 1, 2, 3, 3, 3],
                     [4, 4, 4, 4, 6, 4, 4, 4, 4],
                     [5, 5, 6, 6, 7, 6, 6, 5, 5],
                     [6, 6, 6, 7, 7, 7, 6, 6, 6],
                     [7, 7, 7, 7, 7, 7, 7, 7, 7],
                     [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 2, 4, 6, 6, 7, 8],
                     [0, 1, 1, 2, 4, 6, 7, 7, 8],
                     [0, 1, 1, 1, 6, 7, 7, 7, 8],
                     [0, 1, 2, 2, 4, 6, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8]]]
        assert_array_almost_equal(ft, expected)

    def test_distance_transform_bf02(self):
        "brute force distance transform 2"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = ndimage.distance_transform_bf(data, 'cityblock',
                                                return_indices=True)

        expected = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 1, 2, 2, 2, 1, 0, 0],
                    [0, 0, 1, 2, 3, 2, 1, 0, 0],
                    [0, 0, 1, 2, 2, 2, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        assert_array_almost_equal(out, expected)

        expected = [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 2, 2, 1, 2, 2, 2, 2],
                     [3, 3, 3, 3, 1, 3, 3, 3, 3],
                     [4, 4, 4, 4, 7, 4, 4, 4, 4],
                     [5, 5, 6, 7, 7, 7, 6, 5, 5],
                     [6, 6, 6, 7, 7, 7, 6, 6, 6],
                     [7, 7, 7, 7, 7, 7, 7, 7, 7],
                     [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 2, 4, 6, 6, 7, 8],
                     [0, 1, 1, 1, 4, 7, 7, 7, 8],
                     [0, 1, 1, 1, 4, 7, 7, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8]]]
        assert_array_almost_equal(expected, ft)

    def test_distance_transform_bf03(self):
        "brute force distance transform 3"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = ndimage.distance_transform_bf(data, 'chessboard',
                                                return_indices=True)

        expected = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 1, 1, 2, 1, 1, 0, 0],
                    [0, 0, 1, 2, 2, 2, 1, 0, 0],
                    [0, 0, 1, 1, 2, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        assert_array_almost_equal(out, expected)

        expected = [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 2, 2, 1, 2, 2, 2, 2],
                     [3, 3, 4, 2, 2, 2, 4, 3, 3],
                     [4, 4, 5, 6, 6, 6, 5, 4, 4],
                     [5, 5, 6, 6, 7, 6, 6, 5, 5],
                     [6, 6, 6, 7, 7, 7, 6, 6, 6],
                     [7, 7, 7, 7, 7, 7, 7, 7, 7],
                     [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 2, 5, 6, 6, 7, 8],
                     [0, 1, 1, 2, 6, 6, 7, 7, 8],
                     [0, 1, 1, 2, 6, 7, 7, 7, 8],
                     [0, 1, 2, 2, 6, 6, 7, 7, 8],
                     [0, 1, 2, 4, 5, 6, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8]]]
        assert_array_almost_equal(ft, expected)

    def test_distance_transform_bf04(self):
        "brute force distance transform 4"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        tdt, tft = ndimage.distance_transform_bf(data,
                                                 return_indices=1)
        dts = []
        fts = []
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ndimage.distance_transform_bf(data, distances=dt)
        dts.append(dt)
        ft = ndimage.distance_transform_bf(data,
                            return_distances=False, return_indices=1)
        fts.append(ft)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_bf(data,
             return_distances=False, return_indices=True, indices=ft)
        fts.append(ft)
        dt, ft = ndimage.distance_transform_bf(data,
                                                       return_indices=1)
        dts.append(dt)
        fts.append(ft)
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ft = ndimage.distance_transform_bf(data, distances=dt,
                                                     return_indices=True)
        dts.append(dt)
        fts.append(ft)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        dt = ndimage.distance_transform_bf(data,
                                       return_indices=True, indices=ft)
        dts.append(dt)
        fts.append(ft)
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_bf(data, distances=dt,
                                       return_indices=True, indices=ft)
        dts.append(dt)
        fts.append(ft)
        for dt in dts:
            assert_array_almost_equal(tdt, dt)
        for ft in fts:
            assert_array_almost_equal(tft, ft)

    def test_distance_transform_bf05(self):
        "brute force distance transform 5"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = ndimage.distance_transform_bf(data,
                     'euclidean', return_indices=True, sampling=[2, 2])
        expected = [[0, 0, 0,  0,  0,  0, 0, 0, 0],
                    [0, 0, 0,  0,  0,  0, 0, 0, 0],
                    [0, 0, 0,  4,  4,  4, 0, 0, 0],
                    [0, 0, 4,  8, 16,  8, 4, 0, 0],
                    [0, 0, 4, 16, 32, 16, 4, 0, 0],
                    [0, 0, 4,  8, 16,  8, 4, 0, 0],
                    [0, 0, 0,  4,  4,  4, 0, 0, 0],
                    [0, 0, 0,  0,  0,  0, 0, 0, 0],
                    [0, 0, 0,  0,  0,  0, 0, 0, 0]]
        assert_array_almost_equal(out * out, expected)

        expected = [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 2, 2, 1, 2, 2, 2, 2],
                     [3, 3, 3, 2, 1, 2, 3, 3, 3],
                     [4, 4, 4, 4, 6, 4, 4, 4, 4],
                     [5, 5, 6, 6, 7, 6, 6, 5, 5],
                     [6, 6, 6, 7, 7, 7, 6, 6, 6],
                     [7, 7, 7, 7, 7, 7, 7, 7, 7],
                     [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 2, 4, 6, 6, 7, 8],
                     [0, 1, 1, 2, 4, 6, 7, 7, 8],
                     [0, 1, 1, 1, 6, 7, 7, 7, 8],
                     [0, 1, 2, 2, 4, 6, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8]]]
        assert_array_almost_equal(ft, expected)

    def test_distance_transform_bf06(self):
        "brute force distance transform 6"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = ndimage.distance_transform_bf(data,
                     'euclidean', return_indices=True, sampling=[2, 1])
        expected = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 4, 1, 0, 0, 0],
                    [0, 0, 1, 4, 8, 4, 1, 0, 0],
                    [0, 0, 1, 4, 9, 4, 1, 0, 0],
                    [0, 0, 1, 4, 8, 4, 1, 0, 0],
                    [0, 0, 0, 1, 4, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        assert_array_almost_equal(out * out, expected)

        expected = [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 2, 2, 2, 2, 2, 2, 2],
                     [3, 3, 3, 3, 2, 3, 3, 3, 3],
                     [4, 4, 4, 4, 4, 4, 4, 4, 4],
                     [5, 5, 5, 5, 6, 5, 5, 5, 5],
                     [6, 6, 6, 6, 7, 6, 6, 6, 6],
                     [7, 7, 7, 7, 7, 7, 7, 7, 7],
                     [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 2, 6, 6, 6, 7, 8],
                     [0, 1, 1, 1, 6, 7, 7, 7, 8],
                     [0, 1, 1, 1, 7, 7, 7, 7, 8],
                     [0, 1, 1, 1, 6, 7, 7, 7, 8],
                     [0, 1, 2, 2, 4, 6, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8]]]
        assert_array_almost_equal(ft, expected)

    def test_distance_transform_cdt01(self):
        "chamfer type distance transform 1"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = ndimage.distance_transform_cdt(data,
                                        'cityblock', return_indices=True)
        bf = ndimage.distance_transform_bf(data, 'cityblock')
        assert_array_almost_equal(bf, out)

        expected = [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 2, 1, 1, 1, 2, 2, 2],
                     [3, 3, 2, 1, 1, 1, 2, 3, 3],
                     [4, 4, 4, 4, 1, 4, 4, 4, 4],
                     [5, 5, 5, 5, 7, 7, 6, 5, 5],
                     [6, 6, 6, 6, 7, 7, 6, 6, 6],
                     [7, 7, 7, 7, 7, 7, 7, 7, 7],
                     [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 1, 1, 4, 7, 7, 7, 8],
                     [0, 1, 1, 1, 4, 5, 6, 7, 8],
                     [0, 1, 2, 2, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],]]
        assert_array_almost_equal(ft, expected)

    def test_distance_transform_cdt02(self):
        "chamfer type distance transform 2"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = ndimage.distance_transform_cdt(data, 'chessboard',
                                                 return_indices=True)
        bf = ndimage.distance_transform_bf(data, 'chessboard')
        assert_array_almost_equal(bf, out)

        expected = [[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 2, 2, 1, 1, 1, 2, 2, 2],
                     [3, 3, 2, 2, 1, 2, 2, 3, 3],
                     [4, 4, 3, 2, 2, 2, 3, 4, 4],
                     [5, 5, 4, 6, 7, 6, 4, 5, 5],
                     [6, 6, 6, 6, 7, 7, 6, 6, 6],
                     [7, 7, 7, 7, 7, 7, 7, 7, 7],
                     [8, 8, 8, 8, 8, 8, 8, 8, 8]],
                    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 2, 3, 4, 6, 7, 8],
                     [0, 1, 1, 2, 2, 6, 6, 7, 8],
                     [0, 1, 1, 1, 2, 6, 7, 7, 8],
                     [0, 1, 1, 2, 6, 6, 7, 7, 8],
                     [0, 1, 2, 2, 5, 6, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8],]]
        assert_array_almost_equal(ft, expected)

    def test_distance_transform_cdt03(self):
        "chamfer type distance transform 3"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        tdt, tft = ndimage.distance_transform_cdt(data,
                                                     return_indices=True)
        dts = []
        fts = []
        dt = numpy.zeros(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_cdt(data, distances=dt)
        dts.append(dt)
        ft = ndimage.distance_transform_cdt(data,
                           return_distances=False, return_indices=True)
        fts.append(ft)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_cdt(data,
             return_distances=False, return_indices=True, indices=ft)
        fts.append(ft)
        dt, ft = ndimage.distance_transform_cdt(data,
                                                     return_indices=True)
        dts.append(dt)
        fts.append(ft)
        dt = numpy.zeros(data.shape, dtype=numpy.int32)
        ft = ndimage.distance_transform_cdt(data, distances=dt,
                                                     return_indices=True)
        dts.append(dt)
        fts.append(ft)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        dt = ndimage.distance_transform_cdt(data,
                                       return_indices=True, indices=ft)
        dts.append(dt)
        fts.append(ft)
        dt = numpy.zeros(data.shape, dtype=numpy.int32)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_cdt(data, distances=dt,
                                       return_indices=True, indices=ft)
        dts.append(dt)
        fts.append(ft)
        for dt in dts:
            assert_array_almost_equal(tdt, dt)
        for ft in fts:
            assert_array_almost_equal(tft, ft)

    def test_distance_transform_edt01(self):
        "euclidean distance transform 1"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        out, ft = ndimage.distance_transform_edt(data,
                                                     return_indices=True)
        bf = ndimage.distance_transform_bf(data, 'euclidean')
        assert_array_almost_equal(bf, out)

        dt = ft - numpy.indices(ft.shape[1:], dtype=ft.dtype)
        dt = dt.astype(numpy.float64)
        numpy.multiply(dt, dt, dt)
        dt = numpy.add.reduce(dt, axis=0)
        numpy.sqrt(dt, dt)

        assert_array_almost_equal(bf, dt)

    def test_distance_transform_edt02(self):
        "euclidean distance transform 2"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        tdt, tft = ndimage.distance_transform_edt(data,
                                                     return_indices=True)
        dts = []
        fts = []
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ndimage.distance_transform_edt(data, distances=dt)
        dts.append(dt)
        ft = ndimage.distance_transform_edt(data,
                               return_distances=0, return_indices=True)
        fts.append(ft)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_edt(data,
              return_distances=False,return_indices=True, indices=ft)
        fts.append(ft)
        dt, ft = ndimage.distance_transform_edt(data,
                                                     return_indices=True)
        dts.append(dt)
        fts.append(ft)
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ft = ndimage.distance_transform_edt(data, distances=dt,
                                                     return_indices=True)
        dts.append(dt)
        fts.append(ft)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        dt = ndimage.distance_transform_edt(data,
                                       return_indices=True, indices=ft)
        dts.append(dt)
        fts.append(ft)
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_edt(data, distances=dt,
                                       return_indices=True, indices=ft)
        dts.append(dt)
        fts.append(ft)
        for dt in dts:
            assert_array_almost_equal(tdt, dt)
        for ft in fts:
            assert_array_almost_equal(tft, ft)

    def test_distance_transform_edt03(self):
        "euclidean distance transform 3"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        ref = ndimage.distance_transform_bf(data, 'euclidean',
                                                      sampling=[2, 2])
        out = ndimage.distance_transform_edt(data,
                                                       sampling=[2, 2])
        assert_array_almost_equal(ref, out)

    def test_distance_transform_edt4(self):
        "euclidean distance transform 4"
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]], type)
        ref = ndimage.distance_transform_bf(data, 'euclidean',
                                                      sampling=[2, 1])
        out = ndimage.distance_transform_edt(data,
                                                       sampling=[2, 1])
        assert_array_almost_equal(ref, out)

    def test_distance_transform_edt5(self):
        "Ticket #954"
        out = ndimage.distance_transform_edt(False)
        assert_array_almost_equal(out, [0.])

    def test_generate_structure01(self):
        "generation of a binary structure 1"
        struct = ndimage.generate_binary_structure(0, 1)
        assert_array_almost_equal(struct, 1)

    def test_generate_structure02(self):
        "generation of a binary structure 2"
        struct = ndimage.generate_binary_structure(1, 1)
        assert_array_almost_equal(struct, [1, 1, 1])

    def test_generate_structure03(self):
        "generation of a binary structure 3"
        struct = ndimage.generate_binary_structure(2, 1)
        assert_array_almost_equal(struct, [[0, 1, 0],
                                      [1, 1, 1],
                                      [0, 1, 0]])

    def test_generate_structure04(self):
        "generation of a binary structure 4"
        struct = ndimage.generate_binary_structure(2, 2)
        assert_array_almost_equal(struct, [[1, 1, 1],
                                      [1, 1, 1],
                                      [1, 1, 1]])

    def test_iterate_structure01(self):
        "iterating a structure 1"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        out = ndimage.iterate_structure(struct, 2)
        assert_array_almost_equal(out, [[0, 0, 1, 0, 0],
                                   [0, 1, 1, 1, 0],
                                   [1, 1, 1, 1, 1],
                                   [0, 1, 1, 1, 0],
                                   [0, 0, 1, 0, 0]])

    def test_iterate_structure02(self):
        "iterating a structure 2"
        struct = [[0, 1],
                  [1, 1],
                  [0, 1]]
        out = ndimage.iterate_structure(struct, 2)
        assert_array_almost_equal(out, [[0, 0, 1],
                                   [0, 1, 1],
                                   [1, 1, 1],
                                   [0, 1, 1],
                                   [0, 0, 1]])

    def test_iterate_structure03(self):
        "iterating a structure 3"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        out = ndimage.iterate_structure(struct, 2, 1)
        expected = [[0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 0],
                    [0, 0, 1, 0, 0]]
        assert_array_almost_equal(out[0], expected)
        assert_equal(out[1], [2, 2])

    def test_binary_erosion01(self):
        "binary erosion 1"
        for type in self.types:
            data = numpy.ones([], type)
            out = ndimage.binary_erosion(data)
            assert_array_almost_equal(out, 1)

    def test_binary_erosion02(self):
        "binary erosion 2"
        for type in self.types:
            data = numpy.ones([], type)
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, 1)

    def test_binary_erosion03(self):
        "binary erosion 3"
        for type in self.types:
            data = numpy.ones([1], type)
            out = ndimage.binary_erosion(data)
            assert_array_almost_equal(out, [0])

    def test_binary_erosion04(self):
        "binary erosion 4"
        for type in self.types:
            data = numpy.ones([1], type)
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, [1])

    def test_binary_erosion05(self):
        "binary erosion 5"
        for type in self.types:
            data = numpy.ones([3], type)
            out = ndimage.binary_erosion(data)
            assert_array_almost_equal(out, [0, 1, 0])

    def test_binary_erosion06(self):
        "binary erosion 6"
        for type in self.types:
            data = numpy.ones([3], type)
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, [1, 1, 1])

    def test_binary_erosion07(self):
        "binary erosion 7"
        for type in self.types:
            data = numpy.ones([5], type)
            out = ndimage.binary_erosion(data)
            assert_array_almost_equal(out, [0, 1, 1, 1, 0])

    def test_binary_erosion08(self):
        "binary erosion 8"
        for type in self.types:
            data = numpy.ones([5], type)
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, [1, 1, 1, 1, 1])

    def test_binary_erosion09(self):
        "binary erosion 9"
        for type in self.types:
            data = numpy.ones([5], type)
            data[2] = 0
            out = ndimage.binary_erosion(data)
            assert_array_almost_equal(out, [0, 0, 0, 0, 0])

    def test_binary_erosion10(self):
        "binary erosion 10"
        for type in self.types:
            data = numpy.ones([5], type)
            data[2] = 0
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, [1, 0, 0, 0, 1])

    def test_binary_erosion11(self):
        "binary erosion 11"
        for type in self.types:
            data = numpy.ones([5], type)
            data[2] = 0
            struct = [1, 0, 1]
            out = ndimage.binary_erosion(data, struct,
                                                   border_value=1)
            assert_array_almost_equal(out, [1, 0, 1, 0, 1])

    def test_binary_erosion12(self):
        "binary erosion 12"
        for type in self.types:
            data = numpy.ones([5], type)
            data[2] = 0
            struct = [1, 0, 1]
            out = ndimage.binary_erosion(data, struct,
                                                   border_value=1,
                                                   origin=-1)
            assert_array_almost_equal(out, [0, 1, 0, 1, 1])

    def test_binary_erosion13(self):
        "binary erosion 13"
        for type in self.types:
            data = numpy.ones([5], type)
            data[2] = 0
            struct = [1, 0, 1]
            out = ndimage.binary_erosion(data, struct,
                                                   border_value=1,
                                                   origin=1)
            assert_array_almost_equal(out, [1, 1, 0, 1, 0])

    def test_binary_erosion14(self):
        "binary erosion 14"
        for type in self.types:
            data = numpy.ones([5], type)
            data[2] = 0
            struct = [1, 1]
            out = ndimage.binary_erosion(data, struct,
                                                   border_value=1)
            assert_array_almost_equal(out, [1, 1, 0, 0, 1])

    def test_binary_erosion15(self):
        "binary erosion 15"
        for type in self.types:
            data = numpy.ones([5], type)
            data[2] = 0
            struct = [1, 1]
            out = ndimage.binary_erosion(data, struct,
                                                   border_value=1,
                                                   origin=-1)
            assert_array_almost_equal(out, [1, 0, 0, 1, 1])

    def test_binary_erosion16(self):
        "binary erosion 16"
        for type in self.types:
            data = numpy.ones([1, 1], type)
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, [[1]])

    def test_binary_erosion17(self):
        "binary erosion 17"
        for type in self.types:
            data = numpy.ones([1, 1], type)
            out = ndimage.binary_erosion(data)
            assert_array_almost_equal(out, [[0]])

    def test_binary_erosion18(self):
        "binary erosion 18"
        for type in self.types:
            data = numpy.ones([1, 3], type)
            out = ndimage.binary_erosion(data)
            assert_array_almost_equal(out, [[0, 0, 0]])

    def test_binary_erosion19(self):
        "binary erosion 19"
        for type in self.types:
            data = numpy.ones([1, 3], type)
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, [[1, 1, 1]])

    def test_binary_erosion20(self):
        "binary erosion 20"
        for type in self.types:
            data = numpy.ones([3, 3], type)
            out = ndimage.binary_erosion(data)
            assert_array_almost_equal(out, [[0, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 0]])

    def test_binary_erosion21(self):
        "binary erosion 21"
        for type in self.types:
            data = numpy.ones([3, 3], type)
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, [[1, 1, 1],
                                       [1, 1, 1],
                                       [1, 1, 1]])

    def test_binary_erosion22(self):
        "binary erosion 22"
        expected = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_erosion(data, border_value=1)
            assert_array_almost_equal(out, expected)

    def test_binary_erosion23(self):
        "binary erosion 23"
        struct = ndimage.generate_binary_structure(2, 2)
        expected = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_erosion(data, struct,
                                                   border_value=1)
            assert_array_almost_equal(out, expected)

    def test_binary_erosion24(self):
        "binary erosion 24"
        struct = [[0, 1],
                  [1, 1]]
        expected = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_erosion(data, struct,
                                                   border_value=1)
            assert_array_almost_equal(out, expected)

    def test_binary_erosion25(self):
        "binary erosion 25"
        struct = [[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 0, 1, 1],
                                   [0, 0, 1, 0, 1, 1, 0, 0],
                                   [0, 1, 0, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_erosion(data, struct,
                                                   border_value=1)
            assert_array_almost_equal(out, expected)

    def test_binary_erosion26(self):
        "binary erosion 26"
        struct = [[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1]]
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 1, 1],
                                   [0, 0, 1, 1, 1, 0, 1, 1],
                                   [0, 0, 1, 0, 1, 1, 0, 0],
                                   [0, 1, 0, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 0, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_erosion(data, struct,
                                      border_value=1, origin=(-1, -1))
            assert_array_almost_equal(out, expected)

    def test_binary_erosion27(self):
        "binary erosion 27"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_erosion(data, struct,
                                         border_value=1, iterations=2)
        assert_array_almost_equal(out, expected)

    def test_binary_erosion28(self):
        "binary erosion 28"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], bool)
        out = numpy.zeros(data.shape, bool)
        ndimage.binary_erosion(data, struct, border_value=1,
                                         iterations=2, output=out)
        assert_array_almost_equal(out, expected)

    def test_binary_erosion29(self):
        "binary erosion 29"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numpy.array([[0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0]], bool)
        out = ndimage.binary_erosion(data, struct,
                                         border_value=1, iterations=3)
        assert_array_almost_equal(out, expected)

    def test_binary_erosion30(self):
        "binary erosion 30"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numpy.array([[0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0]], bool)
        out = numpy.zeros(data.shape, bool)
        ndimage.binary_erosion(data, struct, border_value=1,
                                         iterations=3, output=out)
        assert_array_almost_equal(out, expected)

    def test_binary_erosion31(self):
        "binary erosion 31"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 1],
                [0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 1]]
        data = numpy.array([[0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0]], bool)
        out = numpy.zeros(data.shape, bool)
        ndimage.binary_erosion(data, struct, border_value=1,
                          iterations=1, output=out, origin=(-1, -1))
        assert_array_almost_equal(out, expected)

    def test_binary_erosion32(self):
        "binary erosion 32"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_erosion(data, struct,
                                         border_value=1, iterations=2)
        assert_array_almost_equal(out, expected)

    def test_binary_erosion33(self):
        "binary erosion 33"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        mask = [[1, 1, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1]]
        data = numpy.array([[0, 0, 0, 0, 0, 1, 1],
                               [0, 0, 0, 1, 0, 0, 1],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_erosion(data, struct,
                            border_value=1, mask=mask, iterations=-1)
        assert_array_almost_equal(out, expected)

    def test_binary_erosion34(self):
        "binary erosion 34"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        mask = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_erosion(data, struct,
                                            border_value=1, mask=mask)
        assert_array_almost_equal(out, expected)

    def test_binary_erosion35(self):
        "binary erosion 35"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        mask = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
        data = numpy.array([[0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 1, 1, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0],
                               [0, 0, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0, 0]], bool)
        tmp = [[0, 0, 1, 0, 0, 0, 0],
               [0, 1, 1, 1, 0, 0, 0],
               [1, 1, 1, 1, 1, 0, 1],
               [0, 1, 1, 1, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 1]]
        expected = numpy.logical_and(tmp, mask)
        tmp = numpy.logical_and(data, numpy.logical_not(mask))
        expected = numpy.logical_or(expected, tmp)
        out = numpy.zeros(data.shape, bool)
        ndimage.binary_erosion(data, struct, border_value=1,
                                         iterations=1, output=out,
                                         origin=(-1, -1), mask=mask)
        assert_array_almost_equal(out, expected)

    def test_binary_erosion36(self):
        "binary erosion 36"
        struct = [[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]]
        mask = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        tmp = [[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 1, 0, 0, 1],
               [0, 0, 1, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1]]
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 1, 1],
                               [0, 0, 1, 1, 1, 0, 1, 1],
                               [0, 0, 1, 0, 1, 1, 0, 0],
                               [0, 1, 0, 1, 1, 1, 1, 0],
                               [0, 1, 1, 0, 0, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]])
        expected = numpy.logical_and(tmp, mask)
        tmp = numpy.logical_and(data, numpy.logical_not(mask))
        expected = numpy.logical_or(expected, tmp)
        out = ndimage.binary_erosion(data, struct, mask=mask,
                                       border_value=1, origin=(-1, -1))
        assert_array_almost_equal(out, expected)

    def test_binary_dilation01(self):
        "binary dilation 1"
        for type in self.types:
            data = numpy.ones([], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, 1)

    def test_binary_dilation02(self):
        "binary dilation 2"
        for type in self.types:
            data = numpy.zeros([], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, 0)

    def test_binary_dilation03(self):
        "binary dilation 3"
        for type in self.types:
            data = numpy.ones([1], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [1])

    def test_binary_dilation04(self):
        "binary dilation 4"
        for type in self.types:
            data = numpy.zeros([1], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [0])

    def test_binary_dilation05(self):
        "binary dilation 5"
        for type in self.types:
            data = numpy.ones([3], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [1, 1, 1])

    def test_binary_dilation06(self):
        "binary dilation 6"
        for type in self.types:
            data = numpy.zeros([3], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [0, 0, 0])

    def test_binary_dilation07(self):
        "binary dilation 7"
        struct = ndimage.generate_binary_structure(1, 1)
        for type in self.types:
            data = numpy.zeros([3], type)
            data[1] = 1
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [1, 1, 1])

    def test_binary_dilation08(self):
        "binary dilation 8"
        for type in self.types:
            data = numpy.zeros([5], type)
            data[1] = 1
            data[3] = 1
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [1, 1, 1, 1, 1])

    def test_binary_dilation09(self):
        "binary dilation 9"
        for type in self.types:
            data = numpy.zeros([5], type)
            data[1] = 1
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [1, 1, 1, 0, 0])

    def test_binary_dilation10(self):
        "binary dilation 10"
        for type in self.types:
            data = numpy.zeros([5], type)
            data[1] = 1
            out = ndimage.binary_dilation(data, origin=-1)
            assert_array_almost_equal(out, [0, 1, 1, 1, 0])

    def test_binary_dilation11(self):
        "binary dilation 11"
        for type in self.types:
            data = numpy.zeros([5], type)
            data[1] = 1
            out = ndimage.binary_dilation(data, origin=1)
            assert_array_almost_equal(out, [1, 1, 0, 0, 0])

    def test_binary_dilation12(self):
        "binary dilation 12"
        for type in self.types:
            data = numpy.zeros([5], type)
            data[1] = 1
            struct = [1, 0, 1]
            out = ndimage.binary_dilation(data, struct)
            assert_array_almost_equal(out, [1, 0, 1, 0, 0])

    def test_binary_dilation13(self):
        "binary dilation 13"
        for type in self.types:
            data = numpy.zeros([5], type)
            data[1] = 1
            struct = [1, 0, 1]
            out = ndimage.binary_dilation(data, struct,
                                                    border_value=1)
            assert_array_almost_equal(out, [1, 0, 1, 0, 1])

    def test_binary_dilation14(self):
        "binary dilation 14"
        for type in self.types:
            data = numpy.zeros([5], type)
            data[1] = 1
            struct = [1, 0, 1]
            out = ndimage.binary_dilation(data, struct,
                                                    origin=-1)
            assert_array_almost_equal(out, [0, 1, 0, 1, 0])

    def test_binary_dilation15(self):
        "binary dilation 15"
        for type in self.types:
            data = numpy.zeros([5], type)
            data[1] = 1
            struct = [1, 0, 1]
            out = ndimage.binary_dilation(data, struct,
                                            origin=-1, border_value=1)
            assert_array_almost_equal(out, [1, 1, 0, 1, 0])

    def test_binary_dilation16(self):
        "binary dilation 16"
        for type in self.types:
            data = numpy.ones([1, 1], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [[1]])

    def test_binary_dilation17(self):
        "binary dilation 17"
        for type in self.types:
            data = numpy.zeros([1, 1], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [[0]])

    def test_binary_dilation18(self):
        "binary dilation 18"
        for type in self.types:
            data = numpy.ones([1, 3], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [[1, 1, 1]])

    def test_binary_dilation19(self):
        "binary dilation 19"
        for type in self.types:
            data = numpy.ones([3, 3], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [[1, 1, 1],
                               [1, 1, 1],
                               [1, 1, 1]])

    def test_binary_dilation20(self):
        "binary dilation 20"
        for type in self.types:
            data = numpy.zeros([3, 3], type)
            data[1, 1] = 1
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, [[0, 1, 0],
                                       [1, 1, 1],
                                       [0, 1, 0]])

    def test_binary_dilation21(self):
        "binary dilation 21"
        struct = ndimage.generate_binary_structure(2, 2)
        for type in self.types:
            data = numpy.zeros([3, 3], type)
            data[1, 1] = 1
            out = ndimage.binary_dilation(data, struct)
            assert_array_almost_equal(out, [[1, 1, 1],
                                       [1, 1, 1],
                                       [1, 1, 1]])

    def test_binary_dilation22(self):
        "binary dilation 22"
        expected = [[0, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 1, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 1, 0, 0],
                                           [0, 0, 0, 1, 1, 0, 0, 0],
                                           [0, 0, 1, 0, 0, 1, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_dilation(data)
            assert_array_almost_equal(out, expected)

    def test_binary_dilation23(self):
        "binary dilation 23"
        expected = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_dilation(data, border_value=1)
            assert_array_almost_equal(out, expected)

    def test_binary_dilation24(self):
        "binary dilation 24"
        expected = [[1, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_dilation(data, origin=(1, 1))
            assert_array_almost_equal(out, expected)

    def test_binary_dilation25(self):
        "binary dilation 25"
        expected = [[1, 1, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 1, 0, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_dilation(data, origin=(1, 1),
                                                         border_value=1)
            assert_array_almost_equal(out, expected)

    def test_binary_dilation26(self):
        "binary dilation 26"
        struct = ndimage.generate_binary_structure(2, 2)
        expected = [[1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_dilation(data, struct)
            assert_array_almost_equal(out, expected)

    def test_binary_dilation27(self):
        "binary dilation 27"
        struct = [[0, 1],
                  [1, 1]]
        expected = [[0, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_dilation(data, struct)
            assert_array_almost_equal(out, expected)

    def test_binary_dilation28(self):
        "binary dilation 28"
        expected = [[1, 1, 1, 1],
                [1, 0, 0, 1],
                [1, 0, 0, 1],
                [1, 1, 1, 1]]

        for type in self.types:
            data = numpy.array([[0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0]], type)
            out = ndimage.binary_dilation(data, border_value=1)
            assert_array_almost_equal(out, expected)

    def test_binary_dilation29(self):
        "binary dilation 29"
        struct = [[0, 1],
                  [1, 1]]
        expected = [[0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]

        data = numpy.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_dilation(data, struct,
                                                iterations=2)
        assert_array_almost_equal(out, expected)

    def test_binary_dilation30(self):
        "binary dilation 30"
        struct = [[0, 1],
                  [1, 1]]
        expected = [[0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]

        data = numpy.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0]], bool)
        out = numpy.zeros(data.shape, bool)
        ndimage.binary_dilation(data, struct, iterations=2,
                                          output=out)
        assert_array_almost_equal(out, expected)

    def test_binary_dilation31(self):
        "binary dilation 31"
        struct = [[0, 1],
                  [1, 1]]
        expected = [[0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]

        data = numpy.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_dilation(data, struct,
                                                iterations=3)
        assert_array_almost_equal(out, expected)

    def test_binary_dilation32(self):
        "binary dilation 32"
        struct = [[0, 1],
                  [1, 1]]
        expected = [[0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]]

        data = numpy.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0]], bool)
        out = numpy.zeros(data.shape, bool)
        ndimage.binary_dilation(data, struct, iterations=3,
                                          output=out)
        assert_array_almost_equal(out, expected)

    def test_binary_dilation33(self):
        "binary dilation 33"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 1, 1, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        mask = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 1, 1, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        data = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)

        out = ndimage.binary_dilation(data, struct,
                           iterations=-1, mask=mask, border_value=0)
        assert_array_almost_equal(out, expected)

    def test_binary_dilation34(self):
        "binary dilation 34"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        mask = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        data = numpy.zeros(mask.shape, bool)
        out = ndimage.binary_dilation(data, struct,
                          iterations=-1, mask=mask, border_value=1)
        assert_array_almost_equal(out, expected)

    def test_binary_dilation35(self):
        "binary dilation 35"
        tmp = [[1, 1, 0, 0, 0, 0, 1, 1],
               [1, 0, 0, 0, 1, 0, 1, 1],
               [0, 0, 1, 1, 1, 1, 1, 1],
               [0, 1, 1, 1, 1, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [0, 1, 0, 0, 1, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]])
        mask = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        expected = numpy.logical_and(tmp, mask)
        tmp = numpy.logical_and(data, numpy.logical_not(mask))
        expected = numpy.logical_or(expected, tmp)
        for type in self.types:
            data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_dilation(data, mask=mask,
                                        origin=(1, 1), border_value=1)
            assert_array_almost_equal(out, expected)

    def test_binary_propagation01(self):
        "binary propagation 1"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 1, 1, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        mask = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0],
                               [0, 1, 1, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        data = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)

        out = ndimage.binary_propagation(data, struct,
                                            mask=mask, border_value=0)
        assert_array_almost_equal(out, expected)

    def test_binary_propagation02(self):
        "binary propagation 2"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        mask = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        data = numpy.zeros(mask.shape, bool)
        out = ndimage.binary_propagation(data, struct,
                                             mask=mask, border_value=1)
        assert_array_almost_equal(out, expected)

    def test_binary_opening01(self):
        "binary opening 1"
        expected = [[0, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 0, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_opening(data)
            assert_array_almost_equal(out, expected)

    def test_binary_opening02(self):
        "binary opening 2"
        struct = ndimage.generate_binary_structure(2, 2)
        expected = [[1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 0, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_opening(data, struct)
            assert_array_almost_equal(out, expected)

    def test_binary_closing01(self):
        "binary closing 1"
        expected = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 1, 0, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 0, 1, 0, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_closing(data)
            assert_array_almost_equal(out, expected)

    def test_binary_closing02(self):
        "binary closing 2"
        struct = ndimage.generate_binary_structure(2, 2)
        expected = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 0, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_closing(data, struct)
            assert_array_almost_equal(out, expected)

    def test_binary_fill_holes01(self):
        "binary fill holes 1"
        expected = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_fill_holes(data)
        assert_array_almost_equal(out, expected)

    def test_binary_fill_holes02(self):
        "binary fill holes 2"
        expected = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_fill_holes(data)
        assert_array_almost_equal(out, expected)

    def test_binary_fill_holes03(self):
        "binary fill holes 3"
        expected = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 0, 1, 1, 1],
                               [0, 1, 1, 1, 0, 1, 1, 1],
                               [0, 1, 1, 1, 0, 1, 1, 1],
                               [0, 0, 1, 0, 0, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 1, 0, 1, 0, 1, 1, 1],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [0, 0, 1, 0, 0, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0]], bool)
        out = ndimage.binary_fill_holes(data)
        assert_array_almost_equal(out, expected)

    def test_grey_erosion01(self):
        "grey erosion 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        output = ndimage.grey_erosion(array,
                                                footprint=footprint)
        assert_array_almost_equal([[2, 2, 1, 1, 1],
                              [2, 3, 1, 3, 1],
                              [5, 5, 3, 3, 1]], output)

    def test_grey_erosion02(self):
        "grey erosion 2"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        output = ndimage.grey_erosion(array,
                              footprint=footprint, structure=structure)
        assert_array_almost_equal([[2, 2, 1, 1, 1],
                              [2, 3, 1, 3, 1],
                              [5, 5, 3, 3, 1]], output)

    def test_grey_erosion03(self):
        "grey erosion 3"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[1, 1, 1], [1, 1, 1]]
        output = ndimage.grey_erosion(array,
                              footprint=footprint, structure=structure)
        assert_array_almost_equal([[1, 1, 0, 0, 0],
                              [1, 2, 0, 2, 0],
                              [4, 4, 2, 2, 0]], output)

    def test_grey_dilation01(self):
        "grey dilation 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[0, 1, 1], [1, 0, 1]]
        output = ndimage.grey_dilation(array,
                                                 footprint=footprint)
        assert_array_almost_equal([[7, 7, 9, 9, 5],
                              [7, 9, 8, 9, 7],
                              [8, 8, 8, 7, 7]], output)

    def test_grey_dilation02(self):
        "grey dilation 2"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[0, 1, 1], [1, 0, 1]]
        structure = [[0, 0, 0], [0, 0, 0]]
        output = ndimage.grey_dilation(array,
                             footprint=footprint, structure=structure)
        assert_array_almost_equal([[7, 7, 9, 9, 5],
                              [7, 9, 8, 9, 7],
                              [8, 8, 8, 7, 7]], output)

    def test_grey_dilation03(self):
        "grey dilation 3"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[0, 1, 1], [1, 0, 1]]
        structure = [[1, 1, 1], [1, 1, 1]]
        output = ndimage.grey_dilation(array,
                             footprint=footprint, structure=structure)
        assert_array_almost_equal([[8,  8, 10, 10, 6],
                              [8, 10,  9, 10, 8],
                              [9,  9,  9,  8, 8]], output)

    def test_grey_opening01(self):
        "grey opening 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        tmp = ndimage.grey_erosion(array, footprint=footprint)
        expected = ndimage.grey_dilation(tmp, footprint=footprint)
        output = ndimage.grey_opening(array,
                                                footprint=footprint)
        assert_array_almost_equal(expected, output)

    def test_grey_opening02(self):
        "grey opening 2"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = ndimage.grey_erosion(array, footprint=footprint,
                                             structure=structure)
        expected = ndimage.grey_dilation(tmp, footprint=footprint,
                                               structure=structure)
        output = ndimage.grey_opening(array,
                             footprint=footprint, structure=structure)
        assert_array_almost_equal(expected, output)

    def test_grey_closing01(self):
        "grey closing 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        tmp = ndimage.grey_dilation(array, footprint=footprint)
        expected = ndimage.grey_erosion(tmp, footprint=footprint)
        output = ndimage.grey_closing(array,
                                                footprint=footprint)
        assert_array_almost_equal(expected, output)

    def test_grey_closing02(self):
        "grey closing 2"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = ndimage.grey_dilation(array, footprint=footprint,
                                              structure=structure)
        expected = ndimage.grey_erosion(tmp, footprint=footprint,
                                              structure=structure)
        output = ndimage.grey_closing(array,
                              footprint=footprint, structure=structure)
        assert_array_almost_equal(expected, output)

    def test_morphological_gradient01(self):
        "morphological gradient 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp1 = ndimage.grey_dilation(array,
                             footprint=footprint, structure=structure)
        tmp2 = ndimage.grey_erosion(array, footprint=footprint,
                                              structure=structure)
        expected = tmp1 - tmp2
        output = numpy.zeros(array.shape, array.dtype)
        ndimage.morphological_gradient(array,
                footprint=footprint, structure=structure, output=output)
        assert_array_almost_equal(expected, output)

    def test_morphological_gradient02(self):
        "morphological gradient 2"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp1 = ndimage.grey_dilation(array,
                             footprint=footprint, structure=structure)
        tmp2 = ndimage.grey_erosion(array, footprint=footprint,
                                              structure=structure)
        expected = tmp1 - tmp2
        output = ndimage.morphological_gradient(array,
                                footprint=footprint, structure=structure)
        assert_array_almost_equal(expected, output)

    def test_morphological_laplace01(self):
        "morphological laplace 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp1 = ndimage.grey_dilation(array,
                              footprint=footprint, structure=structure)
        tmp2 = ndimage.grey_erosion(array, footprint=footprint,
                                              structure=structure)
        expected = tmp1 + tmp2 - 2 * array
        output = numpy.zeros(array.shape, array.dtype)
        ndimage.morphological_laplace(array, footprint=footprint,
                                     structure=structure, output=output)
        assert_array_almost_equal(expected, output)

    def test_morphological_laplace02(self):
        "morphological laplace 2"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp1 = ndimage.grey_dilation(array,
                             footprint=footprint, structure=structure)
        tmp2 = ndimage.grey_erosion(array, footprint=footprint,
                                              structure=structure)
        expected = tmp1 + tmp2 - 2 * array
        output = ndimage.morphological_laplace(array,
                                footprint=footprint, structure=structure)
        assert_array_almost_equal(expected, output)

    def test_white_tophat01(self):
        "white tophat 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = ndimage.grey_opening(array, footprint=footprint,
                                             structure=structure)
        expected = array - tmp
        output = numpy.zeros(array.shape, array.dtype)
        ndimage.white_tophat(array, footprint=footprint,
                                      structure=structure, output=output)
        assert_array_almost_equal(expected, output)

    def test_white_tophat02(self):
        "white tophat 2"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = ndimage.grey_opening(array, footprint=footprint,
                                             structure=structure)
        expected = array - tmp
        output = ndimage.white_tophat(array, footprint=footprint,
                                                structure=structure)
        assert_array_almost_equal(expected, output)

    def test_black_tophat01(self):
        "black tophat 1"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = ndimage.grey_closing(array, footprint=footprint,
                                             structure=structure)
        expected = tmp - array
        output = numpy.zeros(array.shape, array.dtype)
        ndimage.black_tophat(array, footprint=footprint,
                                      structure=structure, output=output)
        assert_array_almost_equal(expected, output)

    def test_black_tophat02(self):
        "black tophat 2"
        array = numpy.array([[3, 2, 5, 1, 4],
                                [7, 6, 9, 3, 5],
                                [5, 8, 3, 7, 1]])
        footprint = [[1, 0, 1], [1, 1, 0]]
        structure = [[0, 0, 0], [0, 0, 0]]
        tmp = ndimage.grey_closing(array, footprint=footprint,
                                             structure=structure)
        expected = tmp - array
        output = ndimage.black_tophat(array, footprint=footprint,
                                                structure=structure)
        assert_array_almost_equal(expected, output)

    def test_hit_or_miss01(self):
        "binary hit-or-miss transform 1"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 1, 0, 0, 0],
                                   [1, 1, 1, 0, 0],
                                   [0, 1, 0, 1, 1],
                                   [0, 0, 1, 1, 1],
                                   [0, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 1],
                                   [0, 1, 1, 1, 1],
                                   [0, 0, 0, 0, 0]], type)
            out = numpy.zeros(data.shape, bool)
            ndimage.binary_hit_or_miss(data, struct,
                                                 output=out)
            assert_array_almost_equal(expected, out)

    def test_hit_or_miss02(self):
        "binary hit-or-miss transform 2"
        struct = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]
        expected = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 1, 0, 0, 1, 1, 1, 0],
                                   [1, 1, 1, 0, 0, 1, 0, 0],
                                   [0, 1, 0, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_hit_or_miss(data, struct)
            assert_array_almost_equal(expected, out)

    def test_hit_or_miss03(self):
        "binary hit-or-miss transform 3"
        struct1 = [[0, 0, 0],
                   [1, 1, 1],
                   [0, 0, 0]]
        struct2 = [[1, 1, 1],
                   [0, 0, 0],
                   [1, 1, 1]]
        expected = [[0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        for type in self.types:
            data = numpy.array([[0, 1, 0, 0, 1, 1, 1, 0],
                                   [1, 1, 1, 0, 0, 0, 0, 0],
                                   [0, 1, 0, 1, 1, 1, 1, 0],
                                   [0, 0, 1, 1, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 0, 1, 1, 0],
                                   [0, 0, 0, 0, 1, 1, 1, 0],
                                   [0, 1, 1, 1, 1, 1, 1, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]], type)
            out = ndimage.binary_hit_or_miss(data, struct1,
                                              struct2)
            assert_array_almost_equal(expected, out)


class TestDilateFix:

    def setUp(self):
        # dilation related setup
        self.array = numpy.array([[0, 0, 0, 0, 0,],
                                  [0, 0, 0, 0, 0,],
                                  [0, 0, 0, 1, 0,],
                                  [0, 0, 1, 1, 0,],
                                  [0, 0, 0, 0, 0,]], dtype=numpy.uint8)

        self.sq3x3 = numpy.ones((3, 3))
        dilated3x3 = ndimage.binary_dilation(self.array, structure=self.sq3x3)
        self.dilated3x3 = dilated3x3.view(numpy.uint8)

    def test_dilation_square_structure(self):
        result = ndimage.grey_dilation(self.array, structure=self.sq3x3)
        # +1 accounts for difference between grey and binary dilation
        assert_array_almost_equal(result, self.dilated3x3 + 1)

    def test_dilation_scalar_size(self):
        result = ndimage.grey_dilation(self.array, size=3)
        assert_array_almost_equal(result, self.dilated3x3)


#class NDImageTestResult(unittest.TestResult):
#    separator1 = '=' * 70 + '\n'
#    separator2 = '-' * 70 + '\n'
#
#    def __init__(self, stream, verbose):
#        unittest.TestResult.__init__(self)
#        self.stream = stream
#        self.verbose = verbose
#
#    def getDescription(self, test):
#        return test.shortDescription() or str(test)
#
#    def startTest(self, test):
#        unittest.TestResult.startTest(self, test)
#        if self.verbose:
#            self.stream.write(self.getDescription(test))
#            self.stream.write(" ... ")
#
#    def addSuccess(self, test):
#        unittest.TestResult.addSuccess(self, test)
#        if self.verbose:
#            self.stream.write("ok\n")
#
#    def addError(self, test, err):
#        unittest.TestResult.addError(self, test, err)
#        if self.verbose:
#            self.stream.write("ERROR\n")
#
#    def addFailure(self, test, err):
#        unittest.TestResult.addFailure(self, test, err)
#        if self.verbose:
#            self.stream.write("FAIL\n")
#
#    def printErrors(self):
#        self.printErrorList('ERROR', self.errors)
#        self.printErrorList('FAIL', self.failures)
#
#    def printErrorList(self, flavour, errors):
#        for test, err in errors:
#            self.stream.write(self.separator1)
#            description = self.getDescription(test)
#            self.stream.write("%s: %s\n" % (flavour, description))
#            self.stream.write(self.separator2)
#            self.stream.write(err)
#
#def test():
#    if '-v' in sys.argv[1:]:
#        verbose = 1
#    else:
#        verbose = 0
#    suite = unittest.TestSuite()
#    suite.addTest(unittest.makeSuite(NDImageTest))
#    result = NDImageTestResult(sys.stdout, verbose)
#    suite(result)
#    result.printErrors()
#    return len(result.failures), result.testsRun

if __name__ == "__main__":
    run_module_suite()
