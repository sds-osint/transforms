from maltego_trx.decorator_registry import TransformRegistry, TransformSet

Maigret_registry = TransformRegistry(
    owner="stephen@smalldatascience.org",
    author="Stephen",
    host_url="https://localhost:8080",
    seed_ids=["maigret"],
)
Maigret_set = TransformSet("maigret_maltego", "maigret Transforms")
