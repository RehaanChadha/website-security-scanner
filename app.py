from time import perf_counter

from flask import Flask, jsonify, render_template, request

from services.scan_service import run_scan


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/scan")
    def scan():
        submitted_target = request.form.get("target", "")

        try:
            started_at = perf_counter()
            report = run_scan(submitted_target, verbose=False)
            duration_seconds = perf_counter() - started_at
        except ValueError as error:
            return (
                render_template(
                    "index.html",
                    error_message=str(error),
                    submitted_target=submitted_target,
                ),
                400,
            )

        return render_template(
            "index.html",
            report=report,
            report_data=report["report_data"],
            results=report["report_data"]["results"],
            target=report["target"],
            submitted_target=submitted_target,
            duration_seconds=duration_seconds,
        )

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
