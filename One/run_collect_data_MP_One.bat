if exist C:\Users\Jack\anaconda3 (call C:\Users\Jack\anaconda3\Scripts\activate.bat C:\Users\Jack\anaconda3) else (call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3)
cd C:\Code\One
powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61
python collect_data_MP_One.py
powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e
exit