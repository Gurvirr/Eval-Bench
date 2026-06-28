@echo off
REM Run all tasks against gemini-3.5-flash, 3 trials each (sequential)
REM Usage: scripts\run_model.bat

set MODEL=gemini/gemini-3.5-flash
set AGENT=terminus-2
set TRIALS=3

echo Running all tasks with %MODEL% x %TRIALS% trials each...
echo.

harbor run -p samples/leakage-imputation      -a %AGENT% -m %MODEL% -k %TRIALS%
harbor run -p samples/timeseries-lookahead    -a %AGENT% -m %MODEL% -k %TRIALS%
harbor run -p samples/simpsons-paradox        -a %AGENT% -m %MODEL% -k %TRIALS%
harbor run -p samples/join-fanout             -a %AGENT% -m %MODEL% -k %TRIALS%
harbor run -p samples/macro-vs-micro-f1       -a %AGENT% -m %MODEL% -k %TRIALS%
harbor run -p samples/multimodal-excel        -a %AGENT% -m %MODEL% -k %TRIALS%
harbor run -p samples/class-imbalance-accuracy -a %AGENT% -m %MODEL% -k %TRIALS%

echo.
echo All done. Run: python scripts/aggregate_scores.py
