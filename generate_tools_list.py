import os
import re
from urllib.parse import urlparse

import requests
import yaml

package_list = requests.get("https://lfs.koddos.net/lfs/view/development/wget-list-sysv")
match_base_name = re.compile(r"([\w.\-]+)\.((tar)|(patch)|(tgz)|(txz))")
match_name = re.compile(r"([\w\-]+)-[0-9]")


def package_info(packages):
    for package_url in packages:
        elements = urlparse(package_url)
        basename = os.path.basename(elements.path)
        match = match_base_name.search(basename)
        match2 = match_name.search(basename)
        lookup = {
            "expect5.45.4": "expect5",
            "tcl8.6.12-src": "tcl-src",
            "tcl8.6.12-html": "tcl-html",
            "tzdata2022d": "tzdata"
        }
        folder = match.group(1)
        if not match2:
            name = lookup[folder]
        else:
            name = match2.group(1)


        if basename.endswith("patch"):
            name += "-patch"

        yield name, { "url": package_url, "folder": match.group(1) }


with open(os.path.join("vars", "tools.yml"), "w") as fp:
    data = {"tools": {package: info for package, info in package_info(package_list.text.splitlines())}}
    yaml.dump(data, fp)
