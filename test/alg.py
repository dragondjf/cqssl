#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def money(x, n):
	earnings = x * math.pow(2, n-1) * 1.95
	inputs = []
	for i in xrange(n):
		inputs.append(x * math.pow(2, i))
	return earnings - sum(inputs), inputs

print(money(30, 1))
print(money(30, 2))
print(money(30, 3))
print(money(30, 4))
print(money(30, 5))
print(money(30, 6))
print(money(30, 7))
print(money(30, 8))
print(money(30, 9))
print(money(30, 10))
print(money(30, 11))
print(money(30, 12))
