# Makefile for AirBears Supplicant
# This is probably a terrible Makefile.

WIN32_NAME = airbears_supplicant.exe
DARWIN_NAME = AirBears Supplicant.app

NONE: 
	@echo "This Makefile has no default target. Choose from darwin or win32."

win32: dist/$(WIN32_NAME)

dist/$(WIN32_NAME): 
	python -OO build_win32.py py2exe

clean:
	rm *.py{o,c} \
    rm dist/*