from flask import current_app as app
from flask import request
from applications.models import *
from flask_jwt_extended import create_access_token, jwt_required,get_jwt
# from applications.cache import cache

@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.get_json()
    
    admin_name = data.get("admin_name")  # Use `.get()` to avoid KeyError
    password = data.get("password")
   
    # Query using the correct model
    admin_from_db = Admin.query.filter_by(admin_name=admin_name).first()
       
    if admin_from_db:
        if admin_from_db.password == password:
            token = create_access_token(
                identity=admin_name,
                additional_claims={"type": "admin", "id": admin_name}
            )
            return {"access_token": token}, 200
        else:
            return {"message": "Password incorrect"}, 400
    else:
        return {"message": "Admin name incorrect"}, 400
    



@app.route("/admin_dashboard", methods=["GET"])
@jwt_required()
# @cache.memoize(timeout=50)
def admin_dashboard():
    token=get_jwt()
    if not (token["type"]) == "admin":
        return {"message":"login as an admin to access this"},401
    sponsors = Sponsor.query.all()
    json_response = []
    for sponsor in sponsors:
        json_response.append(sponsor.to_json())
    return {"sponsors": json_response}




@app.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    token=get_jwt()
    if not (token["type"]) == "admin":
        return {"message":"login as an admin to access this"},401
    return {"sponsers": [sponsor.to_json() for sponsor in Sponsor.query.all()]}, 200
