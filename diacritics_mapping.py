#!/usr/bin/env python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Running this program:
# $ python3 -m venv venv
# $ source venv/bin/activate
# $ pip install --upgrade pip
# $ pip install --requirement requirements.txt

from bs4 import BeautifulSoup
import http.cookiejar
import pdb
import urllib.request

def get_data(response):
    data_ret = None
    if response.info().get('Content-Encoding') in ['gzip', 'x-gzip']:
        buf = io.BytesIO(response.read())
        fileobj = gzip.GzipFile(fileobj=buf)
        data_ret = fileobj.read()
    elif response.info().get('Content-Encoding') == 'deflate':
        buf = io.BytesIO(response.read())
        try:
            fileobj = io.BytesIO(zlib.decompress(buf))
        except zlib.error:
            fileobj = io.BytesIO(zlib.decompressobj(-zlib.MAX_WBITS).decompress(buf))
        data_ret = fileobj.read()
    elif response.info().get('Content-Encoding') is None:
        data_ret = response.read()
    else:
        print("ERROR: Unknown response!\n")
        sys.exit(1)

    return data_ret

if __name__ == "__main__":

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    print('// Licensed under the Apache License, Version 2.0 (the "License");')
    print('// you may not use this file except in compliance with the License.')
    print('// You may obtain a copy of the License at')
    print('//')
    print('//      http://www.apache.org/licenses/LICENSE-2.0')
    print('//')
    print('// Unless required by applicable law or agreed to in writing, software')
    print('// distributed under the License is distributed on an "AS IS" BASIS,')
    print('// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.')
    print('// See the License for the specific language governing permissions and')
    print('// limitations under the License.')
    print('')
    print('package main')
    print('')

    cj = http.cookiejar.CookieJar()

    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler(),
                                         urllib.request.HTTPHandler(debuglevel=0),
                                         urllib.request.HTTPSHandler(debuglevel=0),
                                         urllib.request.HTTPCookieProcessor(cj))

    root_response = opener.open("https://pinyin.info/unicode/diacritics.html")
    root_data = get_data(root_response)

    root_soup = BeautifulSoup(root_data, features = "html.parser")

    in_table = False

    # There should only be one <table> in the document
    for table_bs in root_soup.findAll('table'):

        # Loop through all the <tr>s in the table
        for tr_bs in table_bs.findAll('tr'):

            # Gather all <td> under the <tr> in a list
            tds = []
            for td_bs in tr_bs.findAll('td'):
                tds += [ td_bs.text ]

            # We only care if there are exactly 4
            if len(tds) != 4:
                continue

            text = tds[3]
            words = text.split()

            # We are looking for (capital|lowercase) [A-Za-z]
            begin_block = False
            if len(words) == 2:
                if words[0] == "capital" or words[0] == "lowercase":
                    if words[1] in alphabet:
                        begin_block = True

            # Is the a start of a unicode grouping?
            if begin_block:
                # Were we previously in a table?
                if in_table:
                    print('}')
                in_table = True

                # Start the variable block
                print('var %s_%s = []rune{' % (words[0], words[1], ))

            # Print the unicode entry
            print("\t'\\u%s', // %s" % (tds[0], text, ))

    print('}')
    print('')

    # Now print out the map of all of the letters of the alphabet
    print ('var mapping = map[rune][]rune{')
    for i in alphabet:
        print ("\t'%c': capital_%c," % (i, i, ))
    print('}')
