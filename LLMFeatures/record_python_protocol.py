"""Record the H006 protocol before opening final evaluation targets."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record


def main():
    info=json.loads((ROOT/'reports/provider_python_v1/current_run.json').read_text())
    entry='''
## H006 — GPT-6.1 Sol: полная Python-функция

2026-10-17. Пользователь поручил проверить полный Python и отдельно проверить корректность валидатора.
Те же small-v1 72813 пары, LightGBM150/31/4threads, seed42; 20 оценённых программ / до300 POST,
3 популяции / до3 исправлений, модель и sampling как H005. Интерфейс modify_features(X, history),
до36 новых числовых признаков + raw15, полный pandas/NumPy без I/O/случайности.
Физически прошлая история и исходные атрибуты; test/labels не доступны функции.
Search128 → top3+raw → confirmation88 → frozen heldout88/val304/test250/all5000.
Промпт содержит рабочий пример, полную схему и лучший предыдущий код с search MAP.
До запуска модельных генераций проверяются валидатор, сопоставление ID/строк, batching,
raw совпадение и числовые pandas/SQL ответы. Реальные отказы требуют отдельного разбора:
валидность и качество не одно и то же, ложные отказы не считать ошибками модели.
Прошлый test просмотрен; повторная оценка, один seed, интерпретировать осторожно.
Подробности: LLMFeatures/PROVIDER_PYTHON_EXPERIMENT.md. Старые эксперименты сохранены.
'''
    for name in ['CONTEXT.md','HYPOTHESES.md']:
        path=ROOT/name
        text=path.read_text(encoding='utf-8-sig')
        if '## H006 — GPT-6.1 Sol: полная Python-функция' not in text:
            first=text.index('\n')+1
            path.write_text(text[:first]+'\n'+entry.lstrip()+'\n'+text[first:],encoding='utf-8')
    record('provider_python_protocol_registered',
           'H006: отдельный Python эксперимент с прежними данными и LightGBM. '
           '300 обращений максимум / 20 оценённых наборов. Валидатор проверяется до генерации, '
           'все реальные отказы будут разобраны отдельно.',
           info['run_id'],status='prepared',artifacts=str(Path(info['directory']).relative_to(ROOT)))


if __name__=='__main__':main()
