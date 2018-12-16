cls

call ..\Scripts\activate
set text_logging=Y
call python -m unittest integration_tests.py 
set test_error=%ERRORLEVEL%

call deactivate
echo test_error = %test_error%
exit /b %test_error%
