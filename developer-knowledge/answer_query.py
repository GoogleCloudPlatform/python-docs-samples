# Copyright 2026 Google LLC
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

# [START developerknowledge_answer_query]
from google.cloud import developer_knowledge_v1


def answer_query(
    query: str = "How do I create a Google Cloud Storage bucket?",
) -> developer_knowledge_v1.AnswerQueryResponse:
    """Answers a developer question grounded in Google developer documentation.

    Args:
        query: The technical question to answer.

    Returns:
        The AnswerQueryResponse containing the grounded answer,
        citations, and references.
    """
    client = developer_knowledge_v1.DeveloperKnowledgeClient()

    request = developer_knowledge_v1.AnswerQueryRequest(
        query=query,
    )

    response = client.answer_query(request=request)

    print(f"Answer:\n{response.answer.answer_text}\n")
    print(f"Citations count: {len(response.answer.citations)}")
    print(f"References count: {len(response.answer.references)}")

    return response


# [END developerknowledge_answer_query]

if __name__ == "__main__":
    answer_query()
