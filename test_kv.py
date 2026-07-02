import json
import tempfile
import unittest
from pathlib import Path

from kv import KeyValueStore


class KeyValueStoreTests(unittest.TestCase):
    def test_set_get_and_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = KeyValueStore(Path(tmp) / "store.json")

            store.set("name", "Ara")
            store.set("count", 3)

            self.assertEqual(store.get("name"), "Ara")
            self.assertEqual(store.get("count"), 3)
            self.assertEqual(store.get("missing", "fallback"), "fallback")

    def test_delete_returns_whether_key_existed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = KeyValueStore(Path(tmp) / "store.json")
            store.set("name", "Ara")

            self.assertTrue(store.delete("name"))
            self.assertFalse(store.delete("name"))
            self.assertIsNone(store.get("name"))

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            store = KeyValueStore(path)
            store.set("enabled", True)
            store.set("items", ["one", "two"])
            store.save()

            loaded = KeyValueStore(path)
            loaded.load()

            self.assertTrue(loaded.get("enabled"))
            self.assertEqual(loaded.get("items"), ["one", "two"])

    def test_load_missing_file_uses_empty_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = KeyValueStore(Path(tmp) / "missing.json")
            store.set("old", "value")

            store.load()

            self.assertIsNone(store.get("old"))

    def test_load_rejects_non_object_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")
            store = KeyValueStore(path)

            with self.assertRaises(ValueError):
                store.load()


if __name__ == "__main__":
    unittest.main()
