from maltego_trx.decorator_registry import TransformRegistry

spotify_registry = TransformRegistry(
    owner="Small Data Science",
    author="Small Data Science",
    host_url="https://localhost:8080",
    seed_ids=[""],
)

spotify_registry.version = "0.1"