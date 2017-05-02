@echo off
setlocal
set exec_dir=%~dp0%
set OMP_NUM_THREADS=1
set PATH=%exec_dir%;H:\Program Files (x86)\gs\gs8.70\bin;H:\Program Files (x86)\gs\gs8.70\lib;%PATH%
set MAGICK_CONFIGURE_PATH=%exec_dir%
"%exec_dir%osra.exe" %*
endlocal
