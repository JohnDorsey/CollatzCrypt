@echo off

set times = 0


:main
title CollatzCrypt_loop_%times%
python CollatzCrypt.py
echo.
echo.
echo.
echo.
echo.
echo.
echo RESTARTING...
echo.
echo.
echo.
echo.
echo.
echo.
set /a times = %times%+1
goto main