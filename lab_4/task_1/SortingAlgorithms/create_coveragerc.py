# create_coveragerc.py
with open('.coveragerc', 'w', encoding='utf-8') as f:
    f.write("""[run]
omit =
    */demo.py
    */main.py
    */Tests/*
    */__pycache__/*
    */venv/*
    */.venv/*
    */.pytest_cache/*

[report]
fail_under = 85
show_missing = True

[html]
directory = htmlcov
title = Test Coverage Report
""")

print("Файл .coveragerc создан в кодировке UTF-8")