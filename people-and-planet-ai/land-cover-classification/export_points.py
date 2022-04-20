# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv

import ee

import create_datasets


def run(
    bucket: str,
    filename_prefix: str,
    points_per_class: int,
    regions_file: str = "data/regions-small.csv",
) -> None:
    with open(regions_file) as f:
        polygons = [
            ee.Geometry.Rectangle([float(x) for x in row.values()])
            for row in csv.DictReader(f)
        ]
    region = ee.Geometry.MultiPolygon(polygons)

    def get_coordinates(point: ee.Feature) -> ee.Feature:
        coords = point.geometry().coordinates()
        return ee.Feature(None, {"lon": coords.get(0), "lat": coords.get(1)})

    points = (
        create_datasets.get_landcover_image()
        .stratifiedSample(
            points_per_class, "landcover", region, scale=10, geometries=True
        )
        .randomColumn("random")
        .sort("random")
        .map(get_coordinates)
    )

    # To look at your active tasks:
    #   https://code.earthengine.google.com/tasks
    task = ee.batch.Export.table.toCloudStorage(
        collection=points,
        description="Land cover training points",
        bucket=bucket,
        fileNamePrefix=filename_prefix,
        selectors=["lat", "lon"],
        fileFormat="CSV",
    )
    task.start()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--filename-prefix", default="land-cover/points")
    parser.add_argument("--points-per-class", default=100, type=int)
    parser.add_argument("--regions-file", default="data/regions.csv")
    parser.add_argument("--project")
    args = parser.parse_args()

    ee.Initialize()

    run(
        bucket=args.bucket,
        filename_prefix=args.filename_prefix,
        points_per_class=args.points_per_class,
        regions_file=args.regions_file,
    )
