import os

EXPECTED_DIRS = [
    'services/api',
    'services/fetcher',
    'services/workers',
    'services/ner',
    'web/app',
    'packages/schemas',
    'infra/helm',
    'infra/terraform',
    'infra/docker',
    'docs',
]

def test_scaffold_directories_exist():
    for path in EXPECTED_DIRS:
        assert os.path.isdir(path), f"{path} missing"
