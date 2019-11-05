from flask import Flask, request
from flask_cors import CORS
from api_management.jaeger import initializejaeger
from flask_opentracing import FlaskTracing
import implementation as implementation


app = Flask(__name__)
CORS(app)

jaeger_tracer = initializejaeger()
tracing = FlaskTracing(jaeger_tracer)


@app.route('/usermanagement/login/', methods=['POST'])
@tracing.trace()
def login():
    with jaeger_tracer.start_active_span(
            'User-management-API endpoint /usermanagement/login/') as scope:
        scope.span.log_kv({'event': 'Calling endpoint /usermanagement/login/', 'request_method': request.method})
        return implementation.checkLogin(request, False)


@app.route('/usermanagement/adminlogin/', methods=['POST'])
@tracing.trace()
def admin_login():
    with jaeger_tracer.start_active_span(
            'User-management-API endpoint /usermanagement/adminlogin/') as scope:
        scope.span.log_kv({'event': 'Calling endpoint /usermanagement/adminlogin/', 'request_method': request.method})
        return implementation.checkLogin(request, True)


@app.route('/usermanagement/register/', methods=['POST'])
@tracing.trace()
def register():
    with jaeger_tracer.start_active_span(
            'User-management-API endpoint /usermanagement/register/') as scope:
        scope.span.log_kv({'event': 'Calling endpoint /usermanagement/register/', 'request_method': request.method})
        return implementation.checkRegister(request)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
