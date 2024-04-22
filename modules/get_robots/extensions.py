from maltego_trx.decorator_registry import TransformRegistry, TransformSet

get_robots_registry = TransformRegistry(
    owner="Stephen",
    author="Stephen",
    host_url="https://localhost:8080",
    seed_ids=["get_robots"],
)
get_robots_set = TransformSet("get_robots", "Get Robots Transforms")
