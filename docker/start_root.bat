FOR /F "delims=" %%i IN ('git rev-parse --show-toplevel') DO set work_dir=%%i
ECHO %work_dir%

docker run -it --rm ^
    -v %work_dir%:/work ^
    -v D:\Data:/data ^
    -w /work ^
    starp/hepynet_root_io:v0.1 bash ^
