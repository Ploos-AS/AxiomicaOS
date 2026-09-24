#!/usr/bin/env python3
"""Static M0.3 qualification gates for the generated Amiga image."""

from pathlib import Path
import argparse, struct

def folded_sum(data):
    total=0
    for off in range(0,1024,4):
        value=struct.unpack_from(">I",data,off)[0]
        old=total
        total=(total+value)&0xffffffff
        if total<old: total=(total+1)&0xffffffff
    return total

p=argparse.ArgumentParser(); p.add_argument("adf",type=Path); a=p.parse_args()
d=a.adf.read_bytes()
assert len(d)==901120, "ADF size"
assert d[:4]==b"DOS\0", "Amiga boot signature"
assert folded_sum(d[:1024])==0xffffffff, "boot checksum"
assert d[1024:1028]==b"AXAM", "AXAM placement"
_,ver,hsize,load,size,expected,flags,reserved=struct.unpack(">4s7I",d[1024:1056])
assert ver==1 and hsize==32, "AXAM version/header"
assert load==0, "relocatable load metadata"
assert flags==0 and reserved==0, "reserved metadata"
body=d[1024+hsize:1024+hsize+size]
assert len(body)==size and (sum(body)&0xffffffff)==expected, "payload checksum"
print("M0.3 STATIC PASS: Amiga ADF/bootblock/AXAM invariants valid")
