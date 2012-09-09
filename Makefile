# Makefile for AirBears Supplicant
# This is probably a terrible Makefile.

WIN32_NAME = airbears_supplicant.exe
DARWIN_NAME = AirBearsSupplicant.app

NONE: 
	@echo "This Makefile has no default target. Choose from darwin or win32."

win32: dist/$(WIN32_NAME)

darwin: dist/$(DARWIN_NAME)

dist/$(WIN32_NAME): 
	python -OO build_win32.py py2exe

dist/$(DARWIN_NAME):
	python -OO build_darwin.py py2app
	# I should find out how to set dest_base equivalent...
	mv "dist/main.app" dist/$(DARWIN_NAME)

clean:
	rm -rf *.py{o,c} build dist
