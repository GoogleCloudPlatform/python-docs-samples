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

    points = (
        create_datasets.get_landcover_image()
        .stratifiedSample(
            points_per_class, "landcover", region, scale=10, geometries=True
        )
        .randomColumn("random")
        .sort("random")
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
    import google.auth

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--filename-prefix", default="land-cover/points")
    parser.add_argument("--points-per-class", default=100, type=int)
    parser.add_argument("--regions-file", default="data/regions.csv")
    parser.add_argument("--project")
    args = parser.parse_args()

    try:
        # For Colab and service accounts we use the default credentials.
        credentials, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        ee.Initialize(credentials, project=args.project)
    except:
        # When running locally EE doesn't like the default credentials.
        # ee.Authenticate()
        ee.Initialize()

    run(
        bucket=args.bucket,
        filename_prefix=args.filename_prefix,
        points_per_class=args.points_per_class,
        regions_file=args.regions_file,
    )
