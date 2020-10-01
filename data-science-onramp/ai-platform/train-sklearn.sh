gcloud ai-platform jobs submit training sklearn-model \
	--package-path trainer/ \
	--module-name trainer.sklearn_model.task \
	--job-dir local
gcloud ai-platform local train \
	--package-path trainer/ \
	--module-name trainer.tfkeras_model.task \
	--job-dir local
deactivate
rm -r env
rm -r local

gcloud ai-platform jobs submit training my_job5 \
    --package-path trainer/ \
	--module-name trainer.sklearn_model.task \
	--job-dir gs://bmiro-test/models/sklearn_dso \
	--runtime-version 2.2 \
	--python-version 3.7 \
	-- \
	--input-path gs://bmiro-test/data/train.csv

gcloud ai-platform jobs submit training my_job6 \
    --package-path trainer/ \
	--module-name trainer.tfkeras_model.task \
	--job-dir gs://bmiro-test/models/tfkeras_dso \
	--runtime-version 2.2 \
	--python-version 3.7 \
	-- \
	--input-path gs://bmiro-test/data/train.csv
