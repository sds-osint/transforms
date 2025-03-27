from maltego_trx.decorator_registry import TransformRegistry, TransformSet

translate_registry = TransformRegistry(
    owner="Small Data Science",
    author="Small Data Science",
    host_url="https://localhost:8080",
    seed_ids=["translate"],
)
Translate_set = TransformSet("Translate", "Translate Transforms")