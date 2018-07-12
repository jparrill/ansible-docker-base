#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
import os, sys
import time
from jinja2 import Environment, FileSystemLoader
from subprocess import check_call
from distutils.spawn import find_executable

class BinaryNotFound(Exception):
    """When spawn tries to find the executable and it cannot, returns
    a None, then this exception will be raised when this happens"""

    def __init__(self, binary):
        self.binary = binary

    def __str__(self):
        return self.binary


class ContImaGen(object):
    """This class creates the container images based on a list of
    dockerfiles using buildah as a software base (requires root)"""

    def gen_cont_img(self, tag, dockerfile):
        bin_name = 'buildah'
        _bin = find_executable(bin_name, path='/usr/bin')
        if _bin:
            print("Creating new image: {}".format(tag))
            _bin = os.path.abspath(_bin)
            command = ['sudo', _bin, 'bud', '-t', tag, '-f', dockerfile, '.']
            return check_call(command, cwd=os.path.dirname(_bin))
        else:
            raise BinaryNotFound(bin_name)
            sys.exit(-1)
        

    def upload_images(self):
        pass


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


    def render(self, filename, var_file):
        env = Environment(loader=FileSystemLoader(self.base_dir), 
                trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(filename)
        build_dir =  self.base_dir + "/spec/"
    
        json_raw = open(var_file).read()
        env_data = json.loads(json_raw)
        pip_packages = self._get_pip_packages(self.base_dir)
    
        for k, v in env_data["os"].iteritems():
            v["os_packages"] = ' '.join(v["os_packages"])
            v["pip_packages"] = pip_packages
            if not os.path.exists(build_dir + v["os_name"]):
                os.makedirs(build_dir + v["os_name"])
            rendered_content = template.render(v)
            file_path = "{}{}/dockerfile.{}{}".format(build_dir, v["os_name"],
                    v["os_name"], v["os_version"]) 
            self._write(file_path, rendered_content.encode('utf-8').strip())
            self.files_created[v["os_tag"]] = file_path
                   

        return self.files_created
    
        
if __name__ == '__main__':
    template_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = "Dockerfile.j2"
    var_file = template_dir + "/env_vars.json"

    templ_gen = TemplateGen(template_dir)
    dfiles = templ_gen.render(template_file, var_file)
    c_img = ContImaGen()
    for tag, dockerfile in dfiles.iteritems():
        print('===============================')
        output = c_img.gen_cont_img(tag, dockerfile)
        print('===============================')


def get_versions(package_name):
    versions = [] 
    url = "https://pypi.python.org/pypi/%s/json" % (package_name,)
    data = json.load(urllib2.urlopen(urllib2.Request(url)))
    versions = data["releases"].keys()
    versions.sort()
    return versions

