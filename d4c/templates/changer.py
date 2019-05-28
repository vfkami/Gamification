#!/usr/bin/env python3
import fileinput
import random
import re

for file in ['segunda',"terca","quarta","quinta","sexta"]:
    with fileinput.FileInput(file+'.html', inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('data-event="event-2"', 'data-event="event-2"'), end='')