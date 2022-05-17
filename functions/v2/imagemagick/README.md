<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google Cloud Platform logo" title="Google Cloud Platform" align="right" height="96" width="96"/>

# Google Cloud Functions ImageMagick sample

This sample shows you how to blur an image using ImageMagick in a
Storage-triggered Cloud Function.

View the [source code][code].

[code]: main.py

## Deploy and Test

1. Follow the [Cloud Functions quickstart guide][quickstart] to setup Cloud
Functions for your project.

1. Clone this repository:

        git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
        cd python-docs-samples/functions/v2/imagemagick

1. Create a Cloud Storage Bucket:

        gsutil mb gs://YOUR_INPUT_BUCKET_NAME

    This storage bucket is used to upload images for the function to check.

1. Create a second Cloud Storage Bucket:

        gsutil mb gs://YOUR_OUTPUT_BUCKET_NAME

     This second storage bucket is used to store blurred images. (Images that are **not** blurred will not be saved to this bucket.)

     The second bucket is necessary because saving the blurred image to the first (input) bucket would cause your function to be invoked a second time with the blurred image itself.

1. Deploy the `blur_offensive_images` function with a Storage trigger:

        gcloud functions deploy blur_offensive_images --trigger-bucket=YOUR_INPUT_BUCKET_NAME --set-env-vars BLURRED_BUCKET_NAME=YOUR_OUTPUT_BUCKET_NAME --runtime python39 --gen2

    * Replace `YOUR_INPUT_BUCKET_NAME` and `YOUR_OUTPUT_BUCKET_NAME` with the names of the respective Cloud Storage Buckets you created earlier.

1.  Upload an offensive image to the Storage bucket, such as this image of
    a flesh-eating zombie: https://cdn.pixabay.com/photo/2015/09/21/14/24/zombie-949916_1280.jpg

1.  Check the logs for the `blur_offensive_images` function in the [Cloud Console][console]

    You should see something like this in your console:

        D      ... User function triggered, starting execution
        I      ... `The image zombie.jpg has been detected as inappropriate.`
        D      ... Execution took 1 ms, user function completed successfully

[quickstart]: https://cloud.google.com/functions/docs/2nd-gen/console-quickstart
[console]: https://console.cloud.google.com/logs/query;query=resource.type%3D%22cloud_run_revision
