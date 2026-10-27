"""Validate the example data in tests/data against the gist schema.

Each file is named <ClassName>-<anything>.yaml and is checked against that
class as linkml-validate checks it, with closed classes. A valid file gives no
result. An invalid file is a counter-example and gives exactly one, the reason
its name states, which REASONS holds as a part of the validator's message.
"""
from pathlib import Path

import pytest
import yaml
from linkml.validator import Validator
from linkml.validator.plugins import JsonschemaValidationPlugin

SCHEMA = Path(__file__).parent.parent / "src" / "gist" / "schema" / "gist.yaml"
DATA = Path(__file__).parent / "data"
VALID = sorted((DATA / "valid").glob("*.yaml"))
INVALID = sorted((DATA / "invalid").glob("*.yaml"))

# A closed class reports every unexpected key in one message, so the count of
# results alone cannot tell one reason from another.
REASONS = {
    "Account-name-not-text": "is not of type 'string', 'null' in /name",
    "Organization-undeclared-slots": "('not_a_real_field', 'undefined_attribute' were unexpected)",
    "Person-slot-outside-domain": "('latitude' was unexpected)",
}


@pytest.fixture(scope="module")
def validator():
    return Validator(SCHEMA, validation_plugins=[JsonschemaValidationPlugin(closed=True)])


def _results(validator, path):
    target_class = path.stem.split("-")[0]
    report = validator.validate(yaml.safe_load(path.read_text()), target_class)
    return [result.message for result in report.results]


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.name)
def test_valid_example_validates(validator, path):
    assert _results(validator, path) == []


@pytest.mark.parametrize("path", INVALID, ids=lambda p: p.name)
def test_invalid_example_fails_once_for_its_reason(validator, path):
    assert path.stem in REASONS, f"{path.name}: add the part of the message it should fail with to REASONS"
    results = _results(validator, path)
    assert len(results) == 1, f"{path.name} should fail for one reason, not {results}"
    assert REASONS[path.stem] in results[0]
