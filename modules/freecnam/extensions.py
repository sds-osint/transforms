from maltego_trx.decorator_registry import TransformRegistry, TransformSet

freecnam_registry = TransformRegistry(
    owner="Small Data Science",
    author="Small Data Science",
    host_url="https://localhost:8080",
    seed_ids=["freecnam"],
)
freecnam_set = TransformSet("FreeCNAM", "FreeCNAM Transforms")