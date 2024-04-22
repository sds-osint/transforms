from maltego_trx.decorator_registry import TransformRegistry, TransformSet

wordpress_registry = TransformRegistry(
    owner="Stephen",
    author="Stephen",
    host_url="https://localhost:8080",
    seed_ids=["wordpress"],
)
wordpress_set = TransformSet("Wordpress", "Wordpress Transforms")