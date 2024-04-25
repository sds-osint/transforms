from maltego_trx.decorator_registry import TransformRegistry, TransformSet

leakcheck_registry = TransformRegistry(
    owner="stephen@smalldatasciecnce.org",
    author="Stephen",
    host_url="https://localhost:8080",
    seed_ids=["leakcheck"],
)
leakcheck_set = TransformSet("leakcheck", "leakcheck Transforms")
