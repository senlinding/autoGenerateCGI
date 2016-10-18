#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Python 2.7
import sys, os, getopt

cgiTable = list()

class CGIEntry:
  def __init__(self):
    self.name = ''
    self.savingFlag = "FALSE"
    self.lockFlag = "UNLOCK"
    self.handleName = ""

fileHeader = "/* Auto-generated files can not be modified ! */\n\n"

def usage():
    print "cgi_handle.py usage:"
    print "cgi_handle.py [json file]"

def getJsonValue(line, name, defaultVal):
    start = line.find(name)
    if start > 0:
        start = line.find(":", start)
        end = line.find(",", start)
        return line[start + 1 : end - 1].strip().strip('/"')

    return defaultVal

def parseCGIJson(file):
    with open(file, "r") as fr:
        while True:
          line = fr.readline()
          if line:
            line = line.strip()
            #print line
            if line.find("{\"name\"") >= 0:
                cgi = CGIEntry()
                cgi.name = getJsonValue(line, "\"name\"", cgi.name)
                cgi.savingFlag = getJsonValue(line, "\"savingFlag\"", cgi.savingFlag)
                cgi.lockFlag = getJsonValue(line, "\"lockFlag\"", cgi.lockFlag)

                #cgi handle name
                var = cgi.name
                handleName = 'CGI_'
                start = 0
                while start >= 0:
                    end = var.find("_", start)
                    if end == -1:
                        end = len(var)
                        handleName += var[start : end].capitalize()
                        break

                    handleName += var[start : end].capitalize()
                    start = end + 1

                cgi.handleName = handleName
                cgiTable.append(cgi)
                #print "cgi name[%s], savingFlag[%s], lockFlag[%s], handleName:[%s]" % (cgi.name, cgi.savingFlag, cgi.lockFlag, cgi.handleName)

          else:
            break

    return 0

def createCGIHandleHead(path):
    with open(path + "/cgi_handle.h", "w") as fw:
        fw.write(fileHeader)
        fw.write("#ifndef __CGI_HANDLE__\n#define __CGI_HANDLE__\n\n")
        fw.write("#include \"httpd.h\"\n\n")

        for cgi in cgiTable:
            fw.write("/* " + cgi.name + " */\n")
            fw.write("SYS_ERR_TYPE " + cgi.handleName + "();\n\n")

        fw.write("\n#endif /* __CGI_HANDLE__ */\n")

def createCGIEntry(path):
    with open(path + "/cgi_entry.c", "w") as fw:
        fw.write(fileHeader)
        fw.write("#include \"httpd.h\"\n")
        fw.write("#include \"cgi_handle.h\"\n\n")
        fw.write("CGI_ENTRY_S g_CGIEntryTables[] = \n{\n")

        for cgi in cgiTable:
            fw.write("\t{\"" + cgi.name + "\", " + cgi.handleName + ", " + cgi.savingFlag + ", " + cgi.lockFlag + "},\n")

        fw.write("\n};\n")

        fw.write("\n\n/* Other c file can't get g_CGIEntryTables length */\n")
        fw.write("INT Httpd_GetCGITablesNum()\n{\n")
        fw.write("\treturn (" + str(len(cgiTable)) + ");\n")
        fw.write("}\n\n")

def createCGIHandle(path):
    with open(path + "/cgi_handle.c", "w") as fw:
        #fw.write(fileHeader)
        fw.write("#include \"httpd.h\"\n")
        fw.write("#include \"cgi.h\"\n")
        fw.write("#include \"cgi_handle.h\"\n\n")

        for cgi in cgiTable:
            fw.write("SYS_ERR_TYPE " + cgi.handleName + "()\n{\n")
            fw.write("\tcJSON *pRoot = cJSON_CreateObject();\n\n")
            fw.write("\tCGI_PRINT_JSON_WITH_MSG(WEB_RET_MSG_SUCCESS, pRoot);\n")
            fw.write("\treturn SYS_OK;\n")
            fw.write("}\n\n")

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        usage()
        sys.exit(1)

    try:	
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "CGI_ENTRY_C_PATH=", "CGI_HANDLE_H_PATH=", "CGI_HANDLE_PATH="])
    except:
        usage()
        sys.exit(1)
        
    for key, val in opts:
        if key == "--CGI_ENTRY_C_PATH":
            cgiEntryPath = val
        elif key == "--CGI_HANDLE_H_PATH":
            cgiHandleHeadPath = val
        elif key == "--CGI_HANDLE_PATH":
            cgiHandlePath = val
        elif key == "h" or key == "--help":
            usage()
            sys.exit(1)

    if args[0].find(".json") > 0:
        print "start parse json ..."
        parseCGIJson(args[0])

        print "start create %s/cgi_entry.c ..." % cgiEntryPath
        createCGIEntry(cgiEntryPath)

        print "start create %s/cgi_handle.h ..." % cgiHandleHeadPath
        createCGIHandleHead(cgiHandleHeadPath)

        print "start create %s/cgi_handle.c ..." % cgiHandlePath
        createCGIHandle(cgiHandlePath)
    else:
        usage()
        sys.exit(1)
