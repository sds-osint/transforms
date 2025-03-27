from maltego_trx.decorator_registry import TransformRegistry, TransformSet

get_robots_registry = TransformRegistry(
    owner="Small Data Science",
    author="Small Data Science",
    host_url="https://localhost:8080",
    seed_ids=["get_robots"],
)
get_robots_set = TransformSet("get_robots", "Get Robots Transforms")
