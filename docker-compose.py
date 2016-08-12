#!/usr/bin/env python

"""Python wrapper to provide docker-compose-like functionality to CentOS 6"""

import sys
import yaml
import os
import getopt
import pprint
# from subprocess import call

# metadata
__author__ = "Steve Jones"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Steve Jones"
__status__ = "Development"

# set up vars
config = {}
compose_file = 'docker-compose.yml'
project_name = os.path.split(os.getcwd())[-1]
docker_commands = []
debug = False

def show_help():
    print "To Do - The help function"


def read_config():
    global config
    # todo; open the config file and read in the yml into a dictionary
    if os.path.isfile("./" + compose_file):
        f = open(compose_file)
        config = yaml.safe_load(f)
        f.close()
        if debug:
            print "Dict: "
            pprint.pprint(config)
        #print len(config['services'])
        build_commands(config)
    else:
        print "Error compose file (" + compose_file + ") not present"
        sys.exit(2)


def build_commands(conf):
    """Builds up the commands to hand to docker"""
    global docker_commands
    for key in config['services']:
        docker_cmd = "docker run -d"
        try:
            links = config['services'][key]['links']
            if links:
                for link in links:
                    docker_cmd += " --link " + project_name + "-" + link
        except KeyError:
            pass
        try:
            ports = config['services'][key]['ports']
            if ports:
                for port in ports:
                    docker_cmd += " -p \"" + port + "\""
        except KeyError:
            pass
        docker_cmd += " --name " + project_name + "-" + key
        try:
            image = config['services'][key]['image']
            docker_cmd += " " + image
        except KeyError:
            print "Critical error: no image specified for service: " + config['services'][key]
        try:
            command = config['services'][key]['command']
            if command:
                docker_cmd += " " + str(command) + " "
        except KeyError:
            pass

        docker_commands.append(docker_cmd)


def main(argv):
    global compose_file, project_name
    try:
        opts, args = getopt.getopt(argv, "hf:p:v", ["file", "project-name", "verbose"])
    except getopt.GetoptError:
        print "Invalid options presented"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            show_help()
        elif opt in ("-f", "--file"):
            compose_file = arg
        elif opt in ("-p", "--project-name"):
            project_name = arg
    print "Running config from " + compose_file + " under project " + project_name
    read_config()
    for cmd in docker_commands:
        if debug:
            print cmd
        else:
            os.system(cmd)

if __name__ == '__main__':
    main(sys.argv[1:])