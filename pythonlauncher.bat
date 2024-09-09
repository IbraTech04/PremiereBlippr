@echo off
set /p args=<"C:\Users\Cheha\Desktop\PremiereBlippr\args.txt"
echo %args%
python "C:\Users\Cheha\Desktop\PremiereBlippr\DetectBlips.py" %args%
pause