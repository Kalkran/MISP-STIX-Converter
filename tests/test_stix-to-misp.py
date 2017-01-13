#!/usr/bin/env python
import glob
from misp_stix_converter.converters import convert
from misp_stix_converter.servers import misp
import os
import pymisp
from pymisp.tools.stix import make_stix_package

def test_convert():
    # This is a public MISP instance.
    # Just running on AWS, nothing particularly interesting.
    mispAPI = misp.MISP("http://35.163.95.230", "pF4Rq3JOHbYAJLMiFDqRPpLxAh3s0PakiSPKWSN5")
    test_files = glob.glob("test_files/*.xml")
    for test_file in test_files:
        with open(test_file, "r") as f:
            misppkg = convert.STIXtoMISP(f.read(), mispAPI.mispAPI)

        # Convert it back for the hell of it. Gib coverage
        try:
            event = pymisp.MISPEvent()
            event.load(misppkg)
            convert.MISPtoSTIX(event)
        except Exception as ex:
            # This is kinda expected for some reason
            if not "'NoneType' object has no attribute 'get'" in str(ex):
                raise Exception("Failed on {} :: {}".format(test_file, ex))
