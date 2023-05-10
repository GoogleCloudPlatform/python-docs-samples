#!/usr/bin/env python

# Copyright 2017 Google LLC. All Rights Reserved.
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

"""This application demonstrates label detection,
explicit content, and shot change detection using the Google Cloud API.

Usage Examples:

    python analyze.py labels gs://cloud-samples-data/video/chicago.mp4
    python analyze.py labels_file resources/cat.mp4
    python analyze.py shots gs://cloud-samples-data/video/gbikes_dinosaur.mp4
    python analyze.py explicit_content \
    gs://cloud-samples-data/video/gbikes_dinosaur.mp4
    python analyze.py text_gcs \
    gs://cloud-samples-data/video/googlework_tiny.mp4
    python analyze.py text_file resources/googlework_tiny.mp4
    python analyze.py objects_gcs gs://cloud-samples-data/video/cat.mp4
    python analyze.py objects_file resources/cat.mp4
"""

import argparse

# [START video_detect_text]
import io

from google.cloud import videointelligence
# [END video_detect_text]


def analyze_explicit_content(path):
    # [START video_analyze_explicit_content]
    """Detects explicit content from the GCS path to a video."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]

    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path}
    )
    print("\nProcessing video for explicit content annotations:")

    result = operation.result(timeout=90)
    print("\nFinished processing.")

    # Retrieve first result because a single video was processed
    for frame in result.annotation_results[0].explicit_annotation.frames:
        likelihood = videointelligence.Likelihood(frame.pornography_likelihood)
        frame_time = frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
        print("Time: {}s".format(frame_time))
        print("\tpornography: {}".format(likelihood.name))
    # [END video_analyze_explicit_content]


def analyze_labels(path):
    # [START video_analyze_labels_gcs]
    """Detects labels given a GCS path."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.LABEL_DETECTION]

    mode = videointelligence.LabelDetectionMode.SHOT_AND_FRAME_MODE
    config = videointelligence.LabelDetectionConfig(label_detection_mode=mode)
    context = videointelligence.VideoContext(label_detection_config=config)

    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path, "video_context": context}
    )
    print("\nProcessing video for label annotations:")

    result = operation.result(timeout=180)
    print("\nFinished processing.")

    # Process video/segment level label annotations
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print("Video label description: {}".format(segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, segment in enumerate(segment_label.segments):
            start_time = (
                segment.segment.start_time_offset.seconds
                + segment.segment.start_time_offset.microseconds / 1e6
            )
            end_time = (
                segment.segment.end_time_offset.seconds
                + segment.segment.end_time_offset.microseconds / 1e6
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = segment.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")

    # Process shot level label annotations
    shot_labels = result.annotation_results[0].shot_label_annotations
    for i, shot_label in enumerate(shot_labels):
        print("Shot label description: {}".format(shot_label.entity.description))
        for category_entity in shot_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, shot in enumerate(shot_label.segments):
            start_time = (
                shot.segment.start_time_offset.seconds
                + shot.segment.start_time_offset.microseconds / 1e6
            )
            end_time = (
                shot.segment.end_time_offset.seconds
                + shot.segment.end_time_offset.microseconds / 1e6
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = shot.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")

    # Process frame level label annotations
    frame_labels = result.annotation_results[0].frame_label_annotations
    for i, frame_label in enumerate(frame_labels):
        print("Frame label description: {}".format(frame_label.entity.description))
        for category_entity in frame_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        # Each frame_label_annotation has many frames,
        # here we print information only about the first frame.
        frame = frame_label.frames[0]
        time_offset = frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
        print("\tFirst frame time offset: {}s".format(time_offset))
        print("\tFirst frame confidence: {}".format(frame.confidence))
        print("\n")
    # [END video_analyze_labels_gcs]


def analyze_labels_file(path):
    # [START video_analyze_labels]
    """Detect labels given a file path."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.LABEL_DETECTION]

    with io.open(path, "rb") as movie:
        input_content = movie.read()

    operation = video_client.annotate_video(
        request={"features": features, "input_content": input_content}
    )
    print("\nProcessing video for label annotations:")

    result = operation.result(timeout=90)
    print("\nFinished processing.")

    # Process video/segment level label annotations
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print("Video label description: {}".format(segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, segment in enumerate(segment_label.segments):
            start_time = (
                segment.segment.start_time_offset.seconds
                + segment.segment.start_time_offset.microseconds / 1e6
            )
            end_time = (
                segment.segment.end_time_offset.seconds
                + segment.segment.end_time_offset.microseconds / 1e6
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = segment.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")

    # Process shot level label annotations
    shot_labels = result.annotation_results[0].shot_label_annotations
    for i, shot_label in enumerate(shot_labels):
        print("Shot label description: {}".format(shot_label.entity.description))
        for category_entity in shot_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, shot in enumerate(shot_label.segments):
            start_time = (
                shot.segment.start_time_offset.seconds
                + shot.segment.start_time_offset.microseconds / 1e6
            )
            end_time = (
                shot.segment.end_time_offset.seconds
                + shot.segment.end_time_offset.microseconds / 1e6
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = shot.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")

    # Process frame level label annotations
    frame_labels = result.annotation_results[0].frame_label_annotations
    for i, frame_label in enumerate(frame_labels):
        print("Frame label description: {}".format(frame_label.entity.description))
        for category_entity in frame_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        # Each frame_label_annotation has many frames,
        # here we print information only about the first frame.
        frame = frame_label.frames[0]
        time_offset = frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
        print("\tFirst frame time offset: {}s".format(time_offset))
        print("\tFirst frame confidence: {}".format(frame.confidence))
        print("\n")
    # [END video_analyze_labels]


def analyze_shots(path):
    # [START video_analyze_shots]
    """Detects camera shot changes."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": path}
    )
    print("\nProcessing video for shot change annotations:")

    result = operation.result(timeout=90)
    print("\nFinished processing.")

    # first result is retrieved because a single video was processed
    for i, shot in enumerate(result.annotation_results[0].shot_annotations):
        start_time = (
            shot.start_time_offset.seconds + shot.start_time_offset.microseconds / 1e6
        )
        end_time = (
            shot.end_time_offset.seconds + shot.end_time_offset.microseconds / 1e6
        )
        print("\tShot {}: {} to {}".format(i, start_time, end_time))
    # [END video_analyze_shots]


def speech_transcription(path):
    # [START video_speech_transcription_gcs]
    """Transcribe speech from a video stored on GCS."""
    from google.cloud import videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.SpeechTranscriptionConfig(
        language_code="en-US", enable_automatic_punctuation=True
    )
    video_context = videointelligence.VideoContext(speech_transcription_config=config)

    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_uri": path,
            "video_context": video_context,
        }
    )

    print("\nProcessing video for speech transcription.")

    result = operation.result(timeout=600)

    # There is only one annotation_result since only
    # one video is processed.
    annotation_results = result.annotation_results[0]
    for speech_transcription in annotation_results.speech_transcriptions:

        # The number of alternatives for each transcription is limited by
        # SpeechTranscriptionConfig.max_alternatives.
        # Each alternative is a different possible transcription
        # and has its own confidence score.
        for alternative in speech_transcription.alternatives:
            print("Alternative level information:")

            print("Transcript: {}".format(alternative.transcript))
            print("Confidence: {}\n".format(alternative.confidence))

            print("Word level information:")
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                print(
                    "\t{}s - {}s: {}".format(
                        start_time.seconds + start_time.microseconds * 1e-6,
                        end_time.seconds + end_time.microseconds * 1e-6,
                        word,
                    )
                )
    # [END video_speech_transcription_gcs]


def video_detect_text_gcs(input_uri):
    # [START video_detect_text_gcs]
    """Detect text in a video stored on GCS."""
    from google.cloud import videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]

    operation = video_client.annotate_video(
        request={"features": features, "input_uri": input_uri}
    )

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=600)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    for text_annotation in annotation_result.text_annotations:
        print("\nText: {}".format(text_annotation.text))

        # Get the first text segment
        text_segment = text_annotation.segments[0]
        start_time = text_segment.segment.start_time_offset
        end_time = text_segment.segment.end_time_offset
        print(
            "start_time: {}, end_time: {}".format(
                start_time.seconds + start_time.microseconds * 1e-6,
                end_time.seconds + end_time.microseconds * 1e-6,
            )
        )

        print("Confidence: {}".format(text_segment.confidence))

        # Show the result for the first frame in this segment.
        frame = text_segment.frames[0]
        time_offset = frame.time_offset
        print(
            "Time offset for the first frame: {}".format(
                time_offset.seconds + time_offset.microseconds * 1e-6
            )
        )
        print("Rotated Bounding Box Vertices:")
        for vertex in frame.rotated_bounding_box.vertices:
            print("\tVertex.x: {}, Vertex.y: {}".format(vertex.x, vertex.y))
    # [END video_detect_text_gcs]


# [START video_detect_text]
def video_detect_text(path):

    """Detect text in a local video."""
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]
    video_context = videointelligence.VideoContext()

    with io.open(path, "rb") as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_content": input_content,
            "video_context": video_context,
        }
    )

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=300)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    for text_annotation in annotation_result.text_annotations:
        print("\nText: {}".format(text_annotation.text))

        # Get the first text segment
        text_segment = text_annotation.segments[0]
        start_time = text_segment.segment.start_time_offset
        end_time = text_segment.segment.end_time_offset
        print(
            "start_time: {}, end_time: {}".format(
                start_time.seconds + start_time.microseconds * 1e-6,
                end_time.seconds + end_time.microseconds * 1e-6,
            )
        )

        print("Confidence: {}".format(text_segment.confidence))

        # Show the result for the first frame in this segment.
        frame = text_segment.frames[0]
        time_offset = frame.time_offset
        print(
            "Time offset for the first frame: {}".format(
                time_offset.seconds + time_offset.microseconds * 1e-6
            )
        )
        print("Rotated Bounding Box Vertices:")
        for vertex in frame.rotated_bounding_box.vertices:
            print("\tVertex.x: {}, Vertex.y: {}".format(vertex.x, vertex.y))
# [END video_detect_text]


def track_objects_gcs(gcs_uri):
    # [START video_object_tracking_gcs]
    """Object tracking in a video stored on GCS."""
    from google.cloud import videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.OBJECT_TRACKING]
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": gcs_uri}
    )
    print("\nProcessing video for object annotations.")

    result = operation.result(timeout=500)
    print("\nFinished processing.\n")

    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations

    for object_annotation in object_annotations:
        print("Entity description: {}".format(object_annotation.entity.description))
        if object_annotation.entity.entity_id:
            print("Entity id: {}".format(object_annotation.entity.entity_id))

        print(
            "Segment: {}s to {}s".format(
                object_annotation.segment.start_time_offset.seconds
                + object_annotation.segment.start_time_offset.microseconds / 1e6,
                object_annotation.segment.end_time_offset.seconds
                + object_annotation.segment.end_time_offset.microseconds / 1e6,
            )
        )

        print("Confidence: {}".format(object_annotation.confidence))

        # Here we print only the bounding box of the first frame in the segment
        frame = object_annotation.frames[0]
        box = frame.normalized_bounding_box
        print(
            "Time offset of the first frame: {}s".format(
                frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
            )
        )
        print("Bounding box position:")
        print("\tleft  : {}".format(box.left))
        print("\ttop   : {}".format(box.top))
        print("\tright : {}".format(box.right))
        print("\tbottom: {}".format(box.bottom))
        print("\n")
    # [END video_object_tracking_gcs]


def track_objects(path):
    # [START video_object_tracking]
    """Object tracking in a local video."""
    from google.cloud import videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.OBJECT_TRACKING]

    with io.open(path, "rb") as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        request={"features": features, "input_content": input_content}
    )
    print("\nProcessing video for object annotations.")

    result = operation.result(timeout=500)
    print("\nFinished processing.\n")

    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations

    # Get only the first annotation for demo purposes.
    object_annotation = object_annotations[0]
    print("Entity description: {}".format(object_annotation.entity.description))
    if object_annotation.entity.entity_id:
        print("Entity id: {}".format(object_annotation.entity.entity_id))

    print(
        "Segment: {}s to {}s".format(
            object_annotation.segment.start_time_offset.seconds
            + object_annotation.segment.start_time_offset.microseconds / 1e6,
            object_annotation.segment.end_time_offset.seconds
            + object_annotation.segment.end_time_offset.microseconds / 1e6,
        )
    )

    print("Confidence: {}".format(object_annotation.confidence))

    # Here we print only the bounding box of the first frame in this segment
    frame = object_annotation.frames[0]
    box = frame.normalized_bounding_box
    print(
        "Time offset of the first frame: {}s".format(
            frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
        )
    )
    print("Bounding box position:")
    print("\tleft  : {}".format(box.left))
    print("\ttop   : {}".format(box.top))
    print("\tright : {}".format(box.right))
    print("\tbottom: {}".format(box.bottom))
    print("\n")
    # [END video_object_tracking]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_labels_parser = subparsers.add_parser("labels", help=analyze_labels.__doc__)
    analyze_labels_parser.add_argument("path")

    analyze_labels_file_parser = subparsers.add_parser(
        "labels_file", help=analyze_labels_file.__doc__
    )
    analyze_labels_file_parser.add_argument("path")

    analyze_explicit_content_parser = subparsers.add_parser(
        "explicit_content", help=analyze_explicit_content.__doc__
    )
    analyze_explicit_content_parser.add_argument("path")

    analyze_shots_parser = subparsers.add_parser("shots", help=analyze_shots.__doc__)
    analyze_shots_parser.add_argument("path")

    transcribe_speech_parser = subparsers.add_parser(
        "transcribe", help=speech_transcription.__doc__
    )
    transcribe_speech_parser.add_argument("path")

    detect_text_parser = subparsers.add_parser(
        "text_gcs", help=video_detect_text_gcs.__doc__
    )
    detect_text_parser.add_argument("path")

    detect_text_file_parser = subparsers.add_parser(
        "text_file", help=video_detect_text.__doc__
    )
    detect_text_file_parser.add_argument("path")

    tack_objects_parser = subparsers.add_parser(
        "objects_gcs", help=track_objects_gcs.__doc__
    )
    tack_objects_parser.add_argument("path")

    tack_objects_file_parser = subparsers.add_parser(
        "objects_file", help=track_objects.__doc__
    )
    tack_objects_file_parser.add_argument("path")

    args = parser.parse_args()

    if args.command == "labels":
        analyze_labels(args.path)
    if args.command == "labels_file":
        analyze_labels_file(args.path)
    if args.command == "shots":
        analyze_shots(args.path)
    if args.command == "explicit_content":
        analyze_explicit_content(args.path)
    if args.command == "transcribe":
        speech_transcription(args.path)
    if args.command == "text_gcs":
        video_detect_text_gcs(args.path)
    if args.command == "text_file":
        video_detect_text(args.path)
    if args.command == "objects_gcs":
        track_objects_gcs(args.path)
    if args.command == "objects_file":
        track_objects(args.path)
