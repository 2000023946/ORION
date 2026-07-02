from src.infrastructure.config.settings import settings
from src.infrastructure.config.mongo_seeder import MongoSeeder
from src.infrastructure.config.seed_data import SEED_DATA
from src.infrastructure.real.http.real_http_client import RealHttpClient
from src.infrastructure.real.mcp_client.llm.llm import LLM
from src.infrastructure.real.mcp_client.parsing.json_adapter import JsonAdapter
from src.infrastructure.real.mcp_client.planning.prompt_factory import PromptFactory
from src.infrastructure.real.mcp_server.tools.db_filter.db_filter_tool import DBFilterTool
from src.infrastructure.real.mcp_server.tools.metadata_filter.mongo_http_client import MongoHttpClient


class DBFilterInfrastructure:
    def __init__(self):
        self.mongo_http_client = None
        self.tool = None

    def build(self) -> DBFilterTool:
        # ----------------------------
        # seed DB
        # ----------------------------
        seeder = MongoSeeder()
        seeder.reset_and_seed(SEED_DATA)

        # ----------------------------
        # DB client
        # ----------------------------
        self.mongo_http_client = MongoHttpClient(
            uri=settings.metadata_db_url,
            db_name=settings.metadata_db_name,
        )
        json_parser=JsonAdapter()
        prompt_factory=PromptFactory()
        real_http_client = RealHttpClient()
        llm = LLM(http_client=real_http_client, json_parser=json_parser)
        # ----------------------------
        # tool (NO LLM REQUIRED HERE)
        # ----------------------------
        self.tool = DBFilterTool(
            http_client=self.mongo_http_client,
            json_parser=json_parser,
            prompt_factory=prompt_factory,
            llm_port=llm
        ) 

        return self.tool