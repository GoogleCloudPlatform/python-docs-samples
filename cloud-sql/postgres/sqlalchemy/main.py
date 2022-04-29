from flask import render_template, Response

from app import get_index_context, init_db, save_vote

############ TABS vs. SPACES App for Cloud Functions ############

db = init_db()


def votes(request):
    if request.method == "GET":
        context = get_index_context(db)
        return render_template("index.html", **context)

    if request.method == "POST":
        team = request.form["team"]
        return save_vote(db, team)

    return Response(
        response="Invalid http request. Method not allowed, must be 'GET' or 'POST'",
        status=400,
    )
