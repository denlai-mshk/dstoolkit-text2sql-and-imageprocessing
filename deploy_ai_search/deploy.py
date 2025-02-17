# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import argparse
from rag_documents import RagDocumentsAISearch
from text_2_sql import Text2SqlAISearch
from text_2_sql_query_cache import Text2SqlQueryCacheAISearch
import logging

logging.basicConfig(level=logging.INFO)


def deploy_config(arguments: argparse.Namespace):
    """Deploy the indexer configuration based on the arguments passed.

    Args:
        arguments (argparse.Namespace): The arguments passed to the script"""
    if arguments.index_type == "rag":
        index_config = RagDocumentsAISearch(
            suffix=arguments.suffix,
            rebuild=arguments.rebuild,
            enable_page_by_chunking=arguments.enable_page_chunking,
        )
    elif arguments.index_type == "text_2_sql":
        index_config = Text2SqlAISearch(
            suffix=arguments.suffix,
            rebuild=arguments.rebuild,
            single_data_dictionary=arguments.single_data_dictionary,
        )
    elif arguments.index_type == "text_2_sql_query_cache":
        index_config = Text2SqlQueryCacheAISearch(
            suffix=arguments.suffix, rebuild=arguments.rebuild
        )
    else:
        raise ValueError("Invalid Indexer Type")

    index_config.deploy()

    if arguments.rebuild:
        index_config.reset_indexer()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument(
        "--index_type",
        type=str,
        required=True,
        help="Type of Indexer want to deploy.",
    )
    parser.add_argument(
        "--rebuild",
        type=bool,
        required=False,
        help="Whether want to delete and rebuild the index",
    )
    parser.add_argument(
        "--enable_page_chunking",
        type=bool,
        required=False,
        help="Whether want to enable chunking by page in adi skill, if no value is passed considered False",
    )
    parser.add_argument(
        "--single_data_dictionary",
        type=bool,
        required=False,
        help="Whether or not a single data dictionary file should be uploaded, or one per entity",
    )
    parser.add_argument(
        "--suffix",
        type=str,
        required=False,
        help="Suffix to be attached to indexer objects",
    )

    args = parser.parse_args()
    deploy_config(args)
