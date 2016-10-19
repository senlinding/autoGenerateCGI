HTTPD_ROOT:=$(subst /http-server,/http-server ,$(shell pwd))
HTTPD_ROOT:=$(word 1, $(HTTPD_ROOT))

CGI_ENTRY_DIR := $(HTTPD_ROOT)/httpd
CGI_HANDLE_HEAD_DIR := $(HTTPD_ROOT)/include/cgi
CGI_HANDLE_DIR := .
CONFIG_DIR := .

all:
	python cgi_handle.py --CGI_ENTRY_C_PATH=$(CGI_ENTRY_DIR) --CGI_HANDLE_H_PATH=$(CGI_HANDLE_HEAD_DIR) --CGI_HANDLE_PATH=$(CGI_HANDLE_DIR)  $(CONFIG_DIR)/cgi_handle.json

.PHONY:clean
clean:
	rm -rf $(CGI_ENTRY_DIR)/cgi_entry.c $(CGI_HANDLE_HEAD_DIR)/cgi_handle.h $(CGI_HANDLE_DIR)/cgi_handle.c

