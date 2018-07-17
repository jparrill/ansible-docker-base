#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
import os, sys
import time
from jinja2 import Environment, FileSystemLoader
from subprocess import check_call
#from distutils.spawn import find_executable
import re
import pprint


class AnsibleHelper(object):
    """This class will contain functions to help recover Ansible info
    regarding versions, branches, releases, etc..."""

    def get_versions(self, package_name):
        versions = [] 
        url = "https://pypi.python.org/pypi/%s/json" % (package_name,)
        data = json.load(urllib2.urlopen(urllib2.Request(url)))
        versions = data["releases"].keys()
        versions.sort()

        return versions

class TemplateGen(object):
    """This class will create all the container specification
    into spec folder, based on env_vars.json file, it returns
    a list with all dockerfiles generated (absolute path)"""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.files_created = {}


    def _write(self, path, content):
        try:
            with open(path, "w") as outfile:
                outfile.write(content)
                outfile.close()
        except IOError:
            print 'Error writing dockerfile template'


    def _get_pip_packages(self, base_dir):
        req_file_raw = open(base_dir + "/requirements.txt").read()
        tmp_list = req_file_raw.replace('\n', ' ').split()
        final_list = []
        for package in tmp_list:
            package = "\"{}\"".format(package)
            final_list.append(package)
        
        return " ".join(final_list)


    def render(self, ansible_versions, filename, var_file):
        env = Environment(loader=FileSystemLoader(self.base_dir), 
                trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(filename)
        build_dir =  self.base_dir + "/spec/"
    
        json_raw = open(var_file).read()
        env_data = json.loads(json_raw)
        pip_packages = self._get_pip_packages(self.base_dir)

        for k, v in env_data["os"].iteritems():
            v["os_packages"] = ' '.join(v["os_packages"])
            v["os_dependencies"] = ' '.join(v["os_dependencies"])
    
        for version in ansible_versions:
            if int(version[0]) >= 2 and not re.search('[a-zA-Z]', version):
                if len(version) > 5:
                    version = version[0:-2]

                if not os.path.exists(build_dir + "ansible-" + version):
                    os.makedirs(build_dir + "ansible-" + version)

                v["pip_packages"] = pip_packages
                v["pip_packages"] += " \"ansible==" + version + "\""

                rendered_content = template.render(v)
                file_path = "{}{}/Dockerfile".format(build_dir,
                        "ansible-" + version) 
                self._write(file_path, rendered_content.encode('utf-8').strip())
                self.files_created["ansible-" + version] = file_path
                   

        return self.files_created
    
        
if __name__ == '__main__':
    template_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = "Dockerfile.j2"
    var_file = template_dir + "/env_vars.json"

    templ_gen = TemplateGen(template_dir)
    ansible_versions = AnsibleHelper().get_versions('ansible')
    dfiles = templ_gen.render(ansible_versions, template_file, var_file)
    pprint.pprint(dfiles)
