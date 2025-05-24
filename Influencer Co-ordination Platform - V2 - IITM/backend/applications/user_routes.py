from flask import current_app as app
from flask import request, jsonify,Blueprint
from applications.models import *
from flask_jwt_extended import create_access_token, jwt_required,get_jwt, get_jwt_identity
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
  

# Sponsor Part Start

@app.route("/create_sponsor", methods=["POST"])
def create_sponsor():
    
    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]
    company_name = data["company_name"]
    industry = data["industry"]
    budget = data["budget"]

    user = User(username=username,password=password,email=email)
    db.session.add(user)
    user_from_db = User.query.filter_by(username=username).first()
    sponsor = Sponsor(user_id = user_from_db.id,company_name=company_name, industry=industry, budget=budget)
    db.session.add(sponsor)
    db.session.commit()
    token=create_access_token(identity=username,additional_claims={"type":"sponsor","id":username})
    return {"access_token": token}, 200



@app.route("/sponsor_login", methods=["POST"])
@jwt_required()
def sponsor_login():
    
    token=get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message":"login as an sponsor to access this"},401
    data = request.get_json()
    username = data.get("username")  # Use .get() to avoid KeyError
    password = data.get("password")
    
    user_from_db = User.query.filter_by(username=username).first()
       
    if user_from_db:
        if user_from_db.password == password:
            return {"message": "sponsor login successfully"}, 200
            
        else:
            return {"message": "password incorrect"}, 400
    else:
        return {"message": "username incorrect"}, 400
    



@app.route("/update_sponsor", methods=["POST"])
@jwt_required()
def update_sponsor():
    
   
    token=get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message":"login as an sponsor to access this"},401
    data = request.json
    sponsor_id = data["sponsor_id"]
    company_name = data["company_name"]
    industry = data["industry"]
    budget = data["budget"]
    
    sponsor = Sponsor.query.get(sponsor_id)
    if not sponsor :
        return{"message":"sponsor doesn't exist !!!"}, 400
    
    sponsor.company_name = company_name
    sponsor.industry = industry
    sponsor.budget = budget
    
    db.session.commit()
    return {"message": "Sponsor updated successfully"}, 200



@app.route("/delete_sponsor", methods=["POST"])
@jwt_required()
def delete_sponsor():
    
    
    token=get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message":"login as an sponsor to access this"},401
    data = request.json
    sponsor_id = data["sponsor_id"]
    
    sponsor = Sponsor.query.get(sponsor_id)
    if not sponsor :
        return{"message":"sponsor doesn't exist !!!"}, 400

    db.session.delete(sponsor)
    db.session.commit()
    return {"message": "Sponsor deleted successfully"}, 200



@app.route("/sponsor_dashboard", methods=["GET"])
@jwt_required()
# @cache.memoize(timeout=50)
def sponsor_dashboard():
    token=get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message":"login as an sponsor to access this"},401
    campaigns = Campaign.query.all()
    json_response = []
    for campaign in campaigns:
        json_response.append(campaign.to_json())
    return {"campaigns": json_response}


@app.route("/sponsor_ads", methods=["GET"])
@jwt_required()
# @cache.memoize(timeout=50)
def sponsor_ads():
    token=get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message":"login as an sponsor to access this"},401
    ads = Ad.query.all()
    json_response = []
    for ad in ads:
        json_response.append(ad.to_json())
    return {"ads": json_response}



# @app.route("/sponsor_dashboard", methods=["GET"])
# @jwt_required()
# def sponsor_dashboard():
#     token = get_jwt()
#     if not (token["type"]) == "sponsor":
#         return {"message": "login as a sponsor to access this"}, 401

#     current_username = token["identity"]
#     user = User.query.filter_by(username=current_username).first()
#     if not user:
#         return {"message": "User not found"}, 404

#     sponsor = Sponsor.query.filter_by(user_id=user.id).first()
#     if not sponsor:
#         return {"message": "Sponsor not found"}, 404

#     return {"sponsers": [sponsor.to_json()]}, 200


# @app.route("/sponsor_profile/<int:sponsor_id>", methods=["GET"])
# @jwt_required()
# def sponsor_profile(sponsor_id):
#     print(f"Fetching profile for sponsor ID: {sponsor_id}")
#     token = get_jwt()
#     if not (token["type"]) == "sponsor":
#         print("Unauthorized access attempt")
#         return {"message": "login as a sponsor to access this"}, 401
    
#     sponsor = Sponsor.query.get(sponsor_id)
#     if not sponsor:
#         print(f"Sponsor ID {sponsor_id} not found")
#         return {"message": "Sponsor not found"}, 404
    
#     print(f"Found sponsor: {sponsor}")
#     return sponsor.to_json(), 200



@app.route("/search_for_sponsor", methods=["POST"])
@jwt_required()
def search_for_sponsor():
    token = get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message": "login as an sponsor to access this"}, 401

    data = request.get_json()
    query_parameter = data["query_parameter"]
    query_string = data["query_string"]

    if query_parameter == "campaign_name":
        # Filter campaigns based on campaign_name
        campaigns = Campaign.query.filter(Campaign.campaign_name == query_string).all()
        return {"data": [campaign.to_json() for campaign in campaigns]}
    
    elif query_parameter == "niche":
        # Filter campaigns based on niche
        campaigns = Influencer.query.filter(Influencer.niche == query_string).all()
        return {"data": [campaign.to_json() for campaign in campaigns]}
    
    elif query_parameter == "reach":
        # Filter campaigns based on reach
        # Assuming reach is a numeric field, convert query_string to int or float if needed
        try:
            reach_value = float(query_string)  # or int(query_string) if reach is an integer
        except ValueError:
            return {"message": "Invalid reach value"}, 400

        campaigns = Influencer.query.filter(Influencer.reach == reach_value).all()
        return {"data": [campaign.to_json() for campaign in campaigns]}
    
    return {"message": "Invalid query parameter"}, 400





@app.route("/add_campaign", methods=["POST"])
@jwt_required()
def add_campaign():
    token = get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message": "Login as a sponsor to access this"}, 401

    try:
        # Access `request.json` directly without parentheses
        data = request.json

        # Check if all necessary fields are provided
        required_fields = ["campaign_name", "sponsor_id", "description", "start_date", "end_date", "budget", "visibility", "goals"]
        for field in required_fields:
            if field not in data:
                return {"message": f"Missing required field: {field}"}, 400

        # Create a new campaign instance
        campaign = Campaign(
            campaign_name=data["campaign_name"],
            sponsor_id=data["sponsor_id"],
            description=data["description"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            budget=data["budget"],
            visibility=data["visibility"],
            goals=data["goals"]
        )

        # Add the campaign to the database
        db.session.add(campaign)
        db.session.commit()

        return {"message": "Campaign created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500



@app.route("/update_campaign", methods=["POST"])
@jwt_required()
def update_campaign():
    
   
    token=get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message":"login as an sponsor to access this"},401
    data = request.json
    # campaign_id = data["campaign_id"]
    campaign_name=data["campaign_name"],
    # campaign_id = data["campaign_id"]
    description=data["description"],
    start_date=data["start_date"],
    end_date=data["end_date"],
    budget=data["budget"],
    visibility=data["visibility"],
    goals=data["goals"]
    
    campaign = Campaign.query.get(campaign_name)
    if not campaign :
        return{"message":"campaign doesn't exist !!!"}, 400
    
    campaign.campaign_name = campaign_name
    campaign.description = description
    campaign.start_date = start_date
    campaign.end_date = end_date
    campaign.budget = budget
    campaign.visibility = visibility
    campaign.goals = goals
    
    db.session.commit()
    return {"message": "Campaign updated successfully"}, 200



@app.route("/delete_campaign", methods=["POST"])
@jwt_required()
def delete_campaign():
    
    token=get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message":"login as an sponsor to access this"},401
    data = request.json
    campaign_id = data["campaign_id"]
    
    campaign = Campaign.query.get(campaign_id)
    
    if not campaign :
        return{"message":"campaign doesn't exist !!!"}, 400

    db.session.delete(campaign)
    db.session.commit()
    return {"message": "campaign deleted successfully"}, 200


@app.route("/add_ad", methods=["POST"])
@jwt_required()
def add_ad():
    token = get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message": "Login as a sponsor to access this"}, 401

    # Access `request.json` without parentheses
    data = request.json

    # Extract data from the JSON payload
    ad_name = data["ad_name"]
    campaign_id = data["campaign_id"]
    content = data["content"]
    sponsor_id = data["sponsor_id"]
    
    # Convert start_date to datetime object
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
    
    budget = data["budget"]
    status = data["status"]
    requirements = data["requirements"]
    target_audience = data["target_audience"]

    # Create a new Ad instance
    ad = Ad(
        ad_name=ad_name,
        campaign_id=campaign_id,
        sponsor_id=sponsor_id,
        content=content,
        start_date=start_date,
        budget=budget,
        status=status,
        requirements=requirements,
        target_audience=target_audience
    )

    # Add the Ad to the database
    db.session.add(ad)
    db.session.commit()
    
    return {"message": "Ad created"}


@app.route("/delete_ad", methods=["POST"])
@jwt_required()
def delete_ad():
    token = get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message": "Login as a sponsor to access this"}, 401

    data = request.json
    ad_id = data.get("ad_id")  # Use .get() to avoid KeyError if 'ad_id' is missing

    # Query the ad by ID
    ad = Ad.query.get(ad_id)
    if not ad:
        return {"message": "Ad doesn't exist!!!"}, 400

    # Delete the ad
    db.session.delete(ad)
    db.session.commit()
    return {"message": "Ad deleted successfully"}, 200



@app.route("/update_ad", methods=["POST"])
@jwt_required()
def update_ad():
    token = get_jwt()
    if not (token["type"]) == "sponsor":
        return {"message": "Login as a sponsor to access this"}, 401

    data = request.json
    ad_id = data.get("ad_id")

    # Fetch the ad by ID
    ad = Ad.query.get(ad_id)
    if not ad:
        return {"message": "Ad doesn't exist!!!"}, 400

    # Update fields if present in the request
    ad.ad_name = data.get("ad_name", ad.ad_name)
    ad.campaign_id = data.get("campaign_id", ad.campaign_id)
    ad.sponsor_id = data.get("sponsor_id", ad.sponsor_id)
    ad.content = data.get("content", ad.content)
    
    # Convert start_date if provided
    if "start_date" in data:
        try:
            ad.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        except ValueError:
            return {"message": "Invalid start_date format. Use YYYY-MM-DD."}, 400
    
    ad.budget = data.get("budget", ad.budget)
    ad.status = data.get("status", ad.status)
    ad.requirements = data.get("requirements", ad.requirements)
    ad.target_audience = data.get("target_audience", ad.target_audience)

    # Commit changes to the database
    db.session.commit()
    return {"message": "Ad updated successfully"}, 200






# Influencer Part Start

@app.route("/create_influencer", methods=["POST"])

def create_influencer():
    
    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]
    category = data["category"]
    niche = data["niche"]
    reach = data["reach"]

    user = User(username=username,password=password,email=email)
    db.session.add(user)
    user_from_db = User.query.filter_by(username=username).first()
    influencer = Influencer(user_id = user_from_db.id,category=category, niche=niche, reach=reach)
    db.session.add(influencer)
    db.session.commit()
    token=create_access_token(identity=username,additional_claims={"type":"influencer","id":username})
    return {"access_token": token}, 200




@app.route("/influencer_login", methods=["POST"])
@jwt_required()
def influencer_login():
    data = request.get_json()
    token=get_jwt()
    if not (token["type"]) == "influencer":
        return {"message":"login as an influencer to access this"},401
    
    username = data.get("username")  # Use `.get()` to avoid KeyError
    password = data.get("password")
    
    user_from_db = User.query.filter_by(username=username).first()
       
    if user_from_db:
        if user_from_db.password == password:
            return {"message": "influencer login successfully"}, 200
            
        else:
            return {"message": "password incorrect"}, 400
    else:
        return {"message": "username incorrect"}, 400




@app.route("/update_influencer", methods=["POST"])
@jwt_required()
def update_influencer():
    
    data = request.json
    token=get_jwt()
    if not (token["type"]) == "influencer":
        return {"message":"login as an influencer to access this"},401
    
    influencer_id = data["influencer_id"]
    category = data["category"]
    niche = data["niche"]
    reach = data["reach"]
    
    influencer = Influencer.query.get(influencer_id)
    if not influencer :
        return{"message":"Influencer doesn't exist !!!"}, 400
    
    influencer.category = category
    influencer.niche = niche
    influencer.reach = reach
    
    db.session.commit()
    return {"message": "Influencer updated successfully"}, 200



@app.route("/delete_influencer", methods=["POST"])
@jwt_required()
def delete_influencer():
    
    data = request.json
    token=get_jwt()
    if not (token["type"]) == "influencer":
        return {"message":"login as an influencer to access this"},401
    
    influencer_id = data["influencer_id"]
    
    influencer = Influencer.query.get(influencer_id)
    if not influencer :
        return{"message":"Influencer doesn't exist !!!"}, 400
    user = User.query.get(influencer.influencer_id)

    db.session.delete(influencer)
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    return {"message": "Influencer deleted successfully"}, 200


@app.route("/influencer_dashboard", methods=["GET"])
@jwt_required()
def influencer_dashboard():
    token=get_jwt()
    if not (token["type"]) == "influencer":
        return {"message":"login as an influencer to access this"},401

    campaigns = Campaign.query.all()
    json_response = []
    for campaign in campaigns:
        json_response.append(campaign.to_json())
    return {"campaigns": json_response}
    # return {"influencer": [influencer.to_json() for influencer in Influencer.query.all()]}, 200


@app.route("/search_for_influencer", methods=["POST"])
@jwt_required()
def search_for_influencer():
    token = get_jwt()
    if not (token["type"]) == "influencer":
        return {"message": "login as an influencer to access this"}, 401

    data = request.get_json()
    query_parameter = data["query_parameter"]
    query_string = data["query_string"]

    if query_parameter == "campaign_name":
        # Filter campaigns based on campaign_name
        campaigns = Campaign.query.filter(Campaign.campaign_name == query_string).all()
        return {"data": [campaign.to_json() for campaign in campaigns]}
    
    # elif query_parameter == "niche":
    #     # Filter campaigns based on niche
    #     campaigns = Influencer.query.filter(Influencer.niche == query_string).all()
    #     return {"data": [campaign.to_json() for campaign in campaigns]}
    
    
    
    return {"message": "Invalid query parameter"}, 400





ad_request_bp = Blueprint('ad_request', __name__)

@ad_request_bp.route('/ad_request', methods=['POST'])
@jwt_required()
def create_ad_request():
    # Get current sponsor from JWT
    sponsor_id = get_jwt_identity()['sponsor_id']
    
    # Get the data from the request
    data = request.get_json()

    message = data.get('message')
    requirements = data.get('requirements')
    payment = data.get('payment')
    campaign_id = data.get('campaign_id')

    # Validate required fields
    if not all([message, requirements, payment, campaign_id]):
        return jsonify({"message": "All fields are required"}), 400

    # Create new ad request
    ad_request = AdRequest(
        sponsor_id=sponsor_id,
        campaign_id=campaign_id,
        message=message,
        requirements=requirements,
        payment=payment,
        status="pending"  # Default status
    )

    try:
        # Add to DB and commit
        db.session.add(ad_request)
        db.session.commit()
        return jsonify({"message": "Ad request submitted successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error submitting ad request: {str(e)}"}), 500
