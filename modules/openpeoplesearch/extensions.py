from maltego_trx.decorator_registry import TransformRegistry, TransformSet

openpeoplesearch_registry = TransformRegistry(
    owner="Stephen",
    author="Stephen",
    host_url="https://localhost:8080",
    seed_ids=["openpeoplesearch"],
)
openpeoplesearch_set = TransformSet("openpeoplesearch", "openpeoplesearch Transforms")