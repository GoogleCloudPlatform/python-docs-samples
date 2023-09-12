# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# isort: split
# [START video_detect_logo]
import io

from google.cloud import videointelligence


def detect_logo(local_file_path="path/to/your/video.mp4"):
    """Performs asynchronous video annotation for logo recognition on a local file."""

    client = videointelligence.VideoIntelligenceServiceClient()

    with io.open(local_file_path, "rb") as f:
        input_content = f.read()
    features = [videointelligence.Feature.LOGO_RECOGNITION]

    operation = client.annotate_video(
        request={"features": features, "input_content": input_content}
    )

    print("Waiting for operation to complete...")
    response = operation.result()

    # Get the first response, since we sent only one video.
    annotation_result = response.annotation_results[0]

    # Annotations for list of logos detected, tracked and recognized in video.
    for logo_recognition_annotation in annotation_result.logo_recognition_annotations:
        entity = logo_recognition_annotation.entity

        # Opaque entity ID. Some IDs may be available in [Google Knowledge Graph
        # Search API](https://developers.google.com/knowledge-graph/).
        print("Entity Id : {}".format(entity.entity_id))

        print("Description : {}".format(entity.description))

        # All logo tracks where the recognized logo appears. Each track corresponds
        # to one logo instance appearing in consecutive frames.
        for track in logo_recognition_annotation.tracks:
            # Video segment of a track.
            print(
                "\n\tStart Time Offset : {}.{}".format(
                    track.segment.start_time_offset.seconds,
                    track.segment.start_time_offset.microseconds * 1000,
                )
            )
            print(
                "\tEnd Time Offset : {}.{}".format(
                    track.segment.end_time_offset.seconds,
                    track.segment.end_time_offset.microseconds * 1000,
                )
            )
            print("\tConfidence : {}".format(track.confidence))

            # The object with timestamp and attributes per frame in the track.
            for timestamped_object in track.timestamped_objects:
                # Normalized Bounding box in a frame, where the object is located.
                normalized_bounding_box = timestamped_object.normalized_bounding_box
                print("\n\t\tLeft : {}".format(normalized_bounding_box.left))
                print("\t\tTop : {}".format(normalized_bounding_box.top))
                print("\t\tRight : {}".format(normalized_bounding_box.right))
                print("\t\tBottom : {}".format(normalized_bounding_box.bottom))

                # Optional. The attributes of the object in the bounding box.
                for attribute in timestamped_object.attributes:
                    print("\n\t\t\tName : {}".format(attribute.name))
                    print("\t\t\tConfidence : {}".format(attribute.confidence))
                    print("\t\t\tValue : {}".format(attribute.value))

            # Optional. Attributes in the track level.
            for track_attribute in track.attributes:
                print("\n\t\tName : {}".format(track_attribute.name))
                print("\t\tConfidence : {}".format(track_attribute.confidence))
                print("\t\tValue : {}".format(track_attribute.value))

        # All video segments where the recognized logo appears. There might be
        # multiple instances of the same logo class appearing in one VideoSegment.
        for segment in logo_recognition_annotation.segments:
            print(
                "\n\tStart Time Offset : {}.{}".format(
                    segment.start_time_offset.seconds,
                    segment.start_time_offset.microseconds * 1000,
                )
            )
            print(
                "\tEnd Time Offset : {}.{}".format(
                    segment.end_time_offset.seconds,
                    segment.end_time_offset.microseconds * 1000,
                )
            )


# [END video_detect_logo]
