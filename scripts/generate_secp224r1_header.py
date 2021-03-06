#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
source_file = os.path.join(script_dir, '../wycheproof/testvectors/ecdh_secp224r1_test.json')
base_file = os.path.join(script_dir, '../header_bases/secp224r1-vectors.h')
target_file = os.path.join(script_dir, '../target/secp224r1-vectors.h')

# Imports a JSON testvector file.
def import_testvector(file):
    
    with open(file) as f:
        vectors = json.loads(f.read())

    return vectors


def string_to_hex_array(string):
    result = "{"
    for i in range(0, len(string)/2):
        result += "0x"
        result += string[i*2]
        result += string[i*2+1]
        if i != len(string)/2-1:
            result += ", "
        if (i+1)%12 == 0:
            result += "\n\t"

    result += "}"
    return result


def format_testcase_to_nss(testcase):
    nss_vector = "\n// Comment: {}".format(testcase["comment"])
    nss_vector += "\n{{{},\n".format(testcase["tcId"]-1)
    nss_vector += "{},\n".format(string_to_hex_array(testcase["public"]))
    nss_vector += "{},\n".format(string_to_hex_array(testcase["private"]))
    nss_vector += "{}}},\n".format(string_to_hex_array(testcase["shared"]))

    # nss_vector += "{},\n".format(str(testcase["result"] == "invalid").lower())
    # nss_vector += "{}}},\n".format(str(case["comment"] == "invalid nonce size").lower())

    return nss_vector


cases = import_testvector(source_file)

with open(base_file) as base:
    header = base.read()

# header = header[:-35]

header += "\n\n// Testvectors from project wycheproof\n"
header += "// <https://github.com/google/wycheproof>\n"
# header += "const chacha_testvector kChaCha20WycheproofVectors[] = {\n"

for group in cases["testGroups"]:
    for case in group["tests"]:
        header += format_testcase_to_nss(case)

header = header[:-2] + "};\n\n"

# header += "#endif  // chachapoly_vectors_h__\n"

with open(target_file, 'w') as target:
    target.write(header)
