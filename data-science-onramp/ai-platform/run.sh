python3 -m venv env
source env/bin/activate
pip install -U pip
pip install -r requirements.txt
gcloud ai-platform local train \
	--package-path trainer/ \
	--module-name trainer.sklearn.task \
	--job-dir local
gcloud ai-platform local train \
	--package-path trainer/ \
	--module-name trainer.tf-keras.task \
	--job-dir local
deactivate
rm -r env
