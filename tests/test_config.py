import yaml

from amo.config import deep_merge, get_config_value, load_config
from amo.context.profiles import get_budget, get_context_profiles


def test_load_config_returns_defaults_when_file_missing(tmp_path):
    config = load_config(tmp_path)
    assert config["version"] == 1
    assert config["context"]["default_profile"] == "quick"
    assert "micro" in config["context"]["profiles"]
    assert config["context"]["profiles"]["quick"]["max_tokens"] == 3000


def test_deep_merge_preserves_nested_defaults():
    base = {"a": {"b": 1, "c": 2}, "d": 3}
    override = {"a": {"b": 99}}
    merged = deep_merge(base, override)
    assert merged["a"]["b"] == 99
    assert merged["a"]["c"] == 2
    assert merged["d"] == 3


def test_deep_merge_adds_new_keys():
    base = {"a": 1}
    override = {"b": 2}
    merged = deep_merge(base, override)
    assert merged["a"] == 1
    assert merged["b"] == 2


def test_deep_merge_replaces_non_dict_with_dict():
    base = {"a": 1}
    override = {"a": {"nested": True}}
    merged = deep_merge(base, override)
    assert merged["a"] == {"nested": True}


def test_config_overrides_profile_budget(tmp_path):
    config_data = {
        "context": {"profiles": {"quick": {"max_tokens": 500}}},
    }
    cfg_path = tmp_path / ".amo.yaml"
    with cfg_path.open("w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    config = load_config(tmp_path)
    assert config["context"]["profiles"]["quick"]["max_tokens"] == 500


def test_get_budget_uses_configured_budget():
    config = {"context": {"profiles": {"quick": {"max_tokens": 500}}}}
    assert get_budget("quick", config=config) == 500


def test_get_budget_falls_back_to_default():
    assert get_budget("quick") == 3000


def test_get_budget_without_config_uses_builtin():
    assert get_budget("quick") == 3000
    assert get_budget("debug") == 8000
    assert get_budget("micro") == 1200


def test_get_budget_unknown_profile_falls_back_to_quick():
    assert get_budget("nonexistent") == 3000


def test_scan_excludes_include_configured_excludes(tmp_path):
    config_data = {
        "scan": {"excludes": ["custom_dir"]},
    }
    cfg_path = tmp_path / ".amo.yaml"
    with cfg_path.open("w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    config = load_config(tmp_path)
    excludes = config["scan"]["excludes"]
    assert "custom_dir" in excludes


def test_get_config_value_dot_notation():
    config = {"a": {"b": {"c": 42}}}
    assert get_config_value(config, "a.b.c") == 42


def test_get_config_value_missing_path():
    config = {"a": 1}
    assert get_config_value(config, "a.b.c", "fallback") == "fallback"


def test_get_config_value_missing_top_key():
    assert get_config_value({}, "missing.key", 99) == 99


def test_unknown_config_keys_are_tolerated(tmp_path):
    config_data = {"unknown_key": "should_not_cause_error"}
    cfg_path = tmp_path / ".amo.yaml"
    with cfg_path.open("w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    config = load_config(tmp_path)
    assert "unknown_key" in config


def test_context_pack_uses_configured_profile_budget(tmp_path):
    config_data = {
        "context": {"profiles": {"quick": {"max_tokens": 500}}},
    }
    cfg_path = tmp_path / ".amo.yaml"
    with cfg_path.open("w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    config = load_config(tmp_path)
    profiles = get_context_profiles(config)
    assert profiles["quick"]["max_tokens"] == 500


def test_context_pack_preserves_builtin_fields_when_config_only_overrides_tokens(tmp_path):
    config_data = {
        "context": {"profiles": {"quick": {"max_tokens": 500}}},
    }
    cfg_path = tmp_path / ".amo.yaml"
    with cfg_path.open("w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    config = load_config(tmp_path)
    profiles = get_context_profiles(config)
    assert profiles["quick"]["max_tokens"] == 500
    assert "purpose" in profiles["quick"]
    assert "agent_rule" in profiles["quick"]


def test_invalid_yaml_fails_clearly(tmp_path):
    cfg_path = tmp_path / ".amo.yaml"
    cfg_path.write_text("{invalid: yaml: broken", encoding="utf-8")
    import pytest

    with pytest.raises(ValueError, match="Invalid YAML"):
        load_config(tmp_path)
