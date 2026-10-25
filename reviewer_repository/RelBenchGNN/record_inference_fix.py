"""Record the report/inference failure and its fix for future sessions."""
from tracking import record

record("bug_fix", "После перехода на один seed обнаружены и исправлены две ошибки: график ошибочно требовал более одного результата для среднего MAP; генератор инференса добавлял pandas до добавления блока hashlib и импорт не попадал в итоговый код. Готовый seed 42 и его метрики сохранены; инференс возобновляется, деревья пока не обучены.",
       artifacts="RelBenchGNN/build_report.py; RelBenchGNN/prepare_inference.py")
