from src.infrastructure.real.mcp_server.tools.metadata_filter.metadata_filter_tool import MetadataFilterTool


class MetadataFilterInfrastructure:
    def __init__(self):
        self.http_client = None
        self.tool = None

    def build(self) -> MetadataFilterTool:
        from src.infrastructure.config.settings import settings
        from src.infrastructure.config.mongo_seeder import MongoSeeder
        from src.infrastructure.config.seed_data import SEED_DATA
        from src.infrastructure.real.mcp_server.tools.metadata_filter.mongo_http_client import MongoHttpClient
        from src.infrastructure.real.mcp_server.tools.metadata_filter.metadata_filter_tool import MetadataFilterTool

        # seed DB
        seeder = MongoSeeder()
        seeder.reset_and_seed(SEED_DATA)

        self.http_client = MongoHttpClient(
            uri=settings.metadata_db_url,
            db_name=settings.metadata_db_name
        )

        self.tool = MetadataFilterTool(http_client=self.http_client)

        return self.tool