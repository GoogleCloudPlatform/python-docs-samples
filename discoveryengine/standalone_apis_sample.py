# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.cloud import discoveryengine_v1 as discoveryengine


def check_grounding_sample(
    project_id: str,
) -> discoveryengine.CheckGroundingResponse:
    # [START genappbuilder_check_grounding]
    from google.cloud import discoveryengine_v1 as discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"

    client = discoveryengine.GroundedGenerationServiceClient()

    # The full resource name of the grounding config.
    # Format: projects/{project_id}/locations/{location}/groundingConfigs/default_grounding_config
    grounding_config = client.grounding_config_path(
        project=project_id,
        location="global",
        grounding_config="default_grounding_config",
    )

    request = discoveryengine.CheckGroundingRequest(
        grounding_config=grounding_config,
        answer_candidate="Titanic was directed by James Cameron. It was released in 1997.",
        facts=[
            discoveryengine.GroundingFact(
                fact_text=(
                    "Titanic is a 1997 American epic romantic disaster movie. It was directed, written,"
                    " and co-produced by James Cameron. The movie is about the 1912 sinking of the"
                    " RMS Titanic. It stars Kate Winslet and Leonardo DiCaprio. The movie was released"
                    " on December 19, 1997. It received positive critical reviews. The movie won 11 Academy"
                    " Awards, and was nominated for fourteen total Academy Awards."
                ),
                attributes={"author": "Simple Wikipedia"},
            ),
            discoveryengine.GroundingFact(
                fact_text=(
                    'James Cameron\'s "Titanic" is an epic, action-packed romance'
                    "set against the ill-fated maiden voyage of the R.M.S. Titanic;"
                    "the pride and joy of the White Star Line and, at the time,"
                    "the largest moving object ever built. "
                    'She was the most luxurious liner of her era -- the "ship of dreams" -- '
                    "which ultimately carried over 1,500 people to their death in the "
                    "ice cold waters of the North Atlantic in the early hours of April 15, 1912."
                ),
                attributes={"author": "Simple Wikipedia"},
            ),
        ],
        grounding_spec=discoveryengine.CheckGroundingSpec(citation_threshold=0.6),
    )

    response = client.check_grounding(request=request)

    # Handle the response
    print(response)
    # [END genappbuilder_check_grounding]

    return response


def rank_sample(
    project_id: str,
) -> discoveryengine.RankResponse:
    # [START genappbuilder_rank]
    from google.cloud import discoveryengine_v1 as discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"

    client = discoveryengine.RankServiceClient()

    # The full resource name of the ranking config.
    # Format: projects/{project_id}/locations/{location}/rankingConfigs/default_ranking_config
    ranking_config = client.ranking_config_path(
        project=project_id,
        location="global",
        ranking_config="default_ranking_config",
    )
    request = discoveryengine.RankRequest(
        ranking_config=ranking_config,
        model="semantic-ranker-default@latest",
        top_n=10,
        query="What is Google Gemini?",
        records=[
            discoveryengine.RankingRecord(
                id="1",
                title="Gemini",
                content="The Gemini zodiac symbol often depicts two figures standing side-by-side.",
            ),
            discoveryengine.RankingRecord(
                id="2",
                title="Gemini",
                content="Gemini is a cutting edge large language model created by Google.",
            ),
            discoveryengine.RankingRecord(
                id="3",
                title="Gemini Constellation",
                content="Gemini is a constellation that can be seen in the night sky.",
            ),
        ],
    )

    response = client.rank(request=request)

    # Handle the response
    print(response)
    # [END genappbuilder_rank]

    return response


def grounded_generation_inline_vais_sample(
    project_number: str,
    engine_id: str,
) -> discoveryengine.GenerateGroundedContentResponse:
    # [START genappbuilder_grounded_generation_inline_vais]
    from google.cloud import discoveryengine_v1 as discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_number = "YOUR_PROJECT_NUMBER"
    # engine_id = "YOUR_ENGINE_ID"

    client = discoveryengine.GroundedGenerationServiceClient()

    request = discoveryengine.GenerateGroundedContentRequest(
        # The full resource name of the location.
        # Format: projects/{project_number}/locations/{location}
        location=client.common_location_path(project=project_number, location="global"),
        generation_spec=discoveryengine.GenerateGroundedContentRequest.GenerationSpec(
            model_id="gemini-2.5-flash",
        ),
        # Conversation between user and model
        contents=[
            discoveryengine.GroundedGenerationContent(
                role="user",
                parts=[
                    discoveryengine.GroundedGenerationContent.Part(
                        text="How did Google do in 2020? Where can I find BigQuery docs?"
                    )
                ],
            )
        ],
        system_instruction=discoveryengine.GroundedGenerationContent(
            parts=[
                discoveryengine.GroundedGenerationContent.Part(
                    text="Add a smiley emoji after the answer."
                )
            ],
        ),
        # What to ground on.
        grounding_spec=discoveryengine.GenerateGroundedContentRequest.GroundingSpec(
            grounding_sources=[
                discoveryengine.GenerateGroundedContentRequest.GroundingSource(
                    inline_source=discoveryengine.GenerateGroundedContentRequest.GroundingSource.InlineSource(
                        grounding_facts=[
                            discoveryengine.GroundingFact(
                                fact_text=(
                                    "The BigQuery documentation can be found at https://cloud.google.com/bigquery/docs/introduction"
                                ),
                                attributes={
                                    "title": "BigQuery Overview",
                                    "uri": "https://cloud.google.com/bigquery/docs/introduction",
                                },
                            ),
                        ]
                    ),
                ),
                discoveryengine.GenerateGroundedContentRequest.GroundingSource(
                    search_source=discoveryengine.GenerateGroundedContentRequest.GroundingSource.SearchSource(
                        # The full resource name of the serving config for a Vertex AI Search App
                        serving_config=f"projects/{project_number}/locations/global/collections/default_collection/engines/{engine_id}/servingConfigs/default_search",
                    ),
                ),
            ]
        ),
    )
    response = client.generate_grounded_content(request)

    # Handle the response
    print(response)
    # [END genappbuilder_grounded_generation_inline_vais]

    return response


def grounded_generation_google_search_sample(
    project_number: str,
) -> discoveryengine.GenerateGroundedContentResponse:
    # [START genappbuilder_grounded_generation_google_search]
    from google.cloud import discoveryengine_v1 as discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_number = "YOUR_PROJECT_NUMBER"

    client = discoveryengine.GroundedGenerationServiceClient()

    request = discoveryengine.GenerateGroundedContentRequest(
        # The full resource name of the location.
        # Format: projects/{project_number}/locations/{location}
        location=client.common_location_path(project=project_number, location="global"),
        generation_spec=discoveryengine.GenerateGroundedContentRequest.GenerationSpec(
            model_id="gemini-2.5-flash",
        ),
        # Conversation between user and model
        contents=[
            discoveryengine.GroundedGenerationContent(
                role="user",
                parts=[
                    discoveryengine.GroundedGenerationContent.Part(
                        text="How much is Google stock?"
                    )
                ],
            )
        ],
        system_instruction=discoveryengine.GroundedGenerationContent(
            parts=[
                discoveryengine.GroundedGenerationContent.Part(text="Be comprehensive.")
            ],
        ),
        # What to ground on.
        grounding_spec=discoveryengine.GenerateGroundedContentRequest.GroundingSpec(
            grounding_sources=[
                discoveryengine.GenerateGroundedContentRequest.GroundingSource(
                    google_search_source=discoveryengine.GenerateGroundedContentRequest.GroundingSource.GoogleSearchSource(
                        # Optional: For Dynamic Retrieval
                        dynamic_retrieval_config=discoveryengine.GenerateGroundedContentRequest.DynamicRetrievalConfiguration(
                            predictor=discoveryengine.GenerateGroundedContentRequest.DynamicRetrievalConfiguration.DynamicRetrievalPredictor(
                                threshold=0.7
                            )
                        )
                    )
                ),
            ]
        ),
    )
    response = client.generate_grounded_content(request)

    # Handle the response
    print(response)
    # [END genappbuilder_grounded_generation_google_search]

    return response


def grounded_generation_streaming_sample(
    project_number: str,
) -> discoveryengine.GenerateGroundedContentResponse:
    # [START genappbuilder_grounded_generation_streaming]
    from google.cloud import discoveryengine_v1 as discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"

    client = discoveryengine.GroundedGenerationServiceClient()

    request = discoveryengine.GenerateGroundedContentRequest(
        # The full resource name of the location.
        # Format: projects/{project_number}/locations/{location}
        location=client.common_location_path(project=project_number, location="global"),
        generation_spec=discoveryengine.GenerateGroundedContentRequest.GenerationSpec(
            model_id="gemini-2.5-flash",
        ),
        # Conversation between user and model
        contents=[
            discoveryengine.GroundedGenerationContent(
                role="user",
                parts=[
                    discoveryengine.GroundedGenerationContent.Part(
                        text="Summarize how to delete a data store in Vertex AI Agent Builder?"
                    )
                ],
            )
        ],
        grounding_spec=discoveryengine.GenerateGroundedContentRequest.GroundingSpec(
            grounding_sources=[
                discoveryengine.GenerateGroundedContentRequest.GroundingSource(
                    google_search_source=discoveryengine.GenerateGroundedContentRequest.GroundingSource.GoogleSearchSource()
                ),
            ]
        ),
    )
    responses = client.stream_generate_grounded_content(iter([request]))

    for response in responses:
        # Handle the response
        print(response)
    # [END genappbuilder_grounded_generation_streaming]

    return response
