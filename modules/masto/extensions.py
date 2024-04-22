from maltego_trx.decorator_registry import TransformRegistry, TransformSet

masto_registry = TransformRegistry(
    owner="stephen@smalldatascience.org",
    author="Stephen",
    host_url="https://localhost:8080",
    seed_ids=["masto"],
)
masto_set = TransformSet("masto", "masto Transforms")
