from maltego_trx.decorator_registry import TransformRegistry, TransformSet

translate_registry = TransformRegistry(
    owner="Stephen",
    author="Stephen",
    host_url="https://localhost:8080",
    seed_ids=["translate"],
)
Translate_set = TransformSet("Translate", "Translate Transforms")