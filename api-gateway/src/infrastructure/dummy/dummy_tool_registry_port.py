class DummyToolRegistryPort:
    def get_tools(self):
        return [
            {"name": "semantic_search"},
            {"name": "web_search"},
            {"name": "merge"}
        ]