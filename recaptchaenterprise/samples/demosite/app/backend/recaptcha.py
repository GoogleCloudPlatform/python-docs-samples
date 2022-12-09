import json

from flask import jsonify, Response

from backend.create_assessment import get_result


def execute_create_assessment(project_id, json_data: json) -> Response:
    print("Inside the backend wrapper")
    threshold_score = 0.50

    try:
        score, reasons = get_result(project_id=project_id,
                                    recaptcha_site_key=json_data["recaptcha_cred"]["sitekey"],
                                    recaptcha_action=json_data["recaptcha_cred"]["action"], token=json_data["recaptcha_cred"]["token"])
        print("Obtained the score from recaptcha")
        if score < threshold_score:
            verdict = "Not a human"
        else:
            verdict = "Human"
        return jsonify({'data': {"score": "{:.12f}".format(score), "verdict": verdict}, "success": "true"})

    except ValueError as e:
        return jsonify({'data': {"error_msg": str(e.__dict__)}, "success": "false"})
    except Exception as e:
        return jsonify({'data': {"error_msg": f"Something happened! Please try again ! {e.__dict__}"}, "success": "false"})

