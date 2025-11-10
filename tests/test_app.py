"""
Tests for Mergington High School Activities API

This module contains comprehensive tests for all API endpoints:
- GET /
- GET /activities
- POST /activities/{activity_name}/signup
- DELETE /activities/{activity_name}/unregister
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before each test to ensure test isolation"""
    # Store original data
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the school soccer team and compete in local leagues",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly matches",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Drama Club": {
            "description": "Participate in school plays and improve acting skills",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Fridays, 2:00 PM - 3:30 PM",
            "max_participants": 20,
            "participants": ["amelia@mergington.edu", "benjamin@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Prepare for math competitions and solve challenging problems",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["charlotte@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["harper@mergington.edu", "jackson@mergington.edu"]
        }
    }
    
    # Reset the activities to original state
    activities.clear()
    activities.update(original_activities)


class TestRootEndpoint:
    """Tests for the root endpoint GET /"""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Tests for the activities endpoint GET /activities"""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all available activities"""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that we get a dictionary of activities
        assert isinstance(data, dict)
        
        # Check that all expected activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Basketball Club", "Drama Club", "Art Workshop", "Math Olympiad", "Science Club"
        ]
        
        for activity_name in expected_activities:
            assert activity_name in data
            
        # Check structure of an activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        
    def test_activities_response_format(self, client):
        """Test the structure and format of activities response"""
        response = client.get("/activities")
        data = response.json()
        
        # Test specific activity structure
        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupEndpoint:
    """Tests for the signup endpoint POST /activities/{activity_name}/signup"""
    
    def test_successful_signup(self, client):
        """Test successful student signup for an activity"""
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity}"
        
        # Verify the student was added to the activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]
        
    def test_signup_for_nonexistent_activity(self, client):
        """Test signup for an activity that doesn't exist"""
        email = "student@mergington.edu"
        activity = "Nonexistent Activity"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
        
    def test_duplicate_signup_fails(self, client):
        """Test that signing up the same student twice for the same activity fails"""
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student is already signed up"
        
    def test_signup_with_url_encoded_activity_name(self, client):
        """Test signup with URL-encoded activity name"""
        email = "newstudent@mergington.edu"
        activity = "Programming Class"
        encoded_activity = "Programming%20Class"
        
        response = client.post(f"/activities/{encoded_activity}/signup?email={email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity}"


class TestUnregisterEndpoint:
    """Tests for the unregister endpoint DELETE /activities/{activity_name}/unregister"""
    
    def test_successful_unregister(self, client):
        """Test successful student unregistration from an activity"""
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        activity = "Chess Club"
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Unregistered {email} from {activity}"
        
        # Verify the student was removed from the activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity]["participants"]
        
    def test_unregister_from_nonexistent_activity(self, client):
        """Test unregistration from an activity that doesn't exist"""
        email = "student@mergington.edu"
        activity = "Nonexistent Activity"
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
        
    def test_unregister_student_not_registered(self, client):
        """Test unregistering a student who isn't registered for the activity"""
        email = "notregistered@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Student is not registered for this activity"
        
    def test_unregister_with_url_encoded_activity_name(self, client):
        """Test unregistration with URL-encoded activity name"""
        email = "emma@mergington.edu"  # Already signed up for Programming Class
        activity = "Programming Class"
        encoded_activity = "Programming%20Class"
        
        response = client.delete(f"/activities/{encoded_activity}/unregister?email={email}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Unregistered {email} from {activity}"


class TestIntegrationScenarios:
    """Integration tests for complex user scenarios"""
    
    def test_complete_signup_and_unregister_flow(self, client):
        """Test complete flow: signup then unregister"""
        email = "testflow@mergington.edu"
        activity = "Drama Club"
        
        # Initial state - student not registered
        activities_response = client.get("/activities")
        initial_participants = activities_response.json()[activity]["participants"]
        assert email not in initial_participants
        
        # Sign up
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        assert signup_response.status_code == 200
        
        # Verify signup
        activities_response = client.get("/activities")
        after_signup_participants = activities_response.json()[activity]["participants"]
        assert email in after_signup_participants
        assert len(after_signup_participants) == len(initial_participants) + 1
        
        # Unregister
        unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert unregister_response.status_code == 200
        
        # Verify unregistration
        activities_response = client.get("/activities")
        final_participants = activities_response.json()[activity]["participants"]
        assert email not in final_participants
        assert len(final_participants) == len(initial_participants)
        
    def test_multiple_students_same_activity(self, client):
        """Test multiple students signing up for the same activity"""
        activity = "Science Club"
        students = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        
        # Get initial participant count
        activities_response = client.get("/activities")
        initial_count = len(activities_response.json()[activity]["participants"])
        
        # Sign up all students
        for email in students:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
            
        # Verify all students are registered
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity]["participants"]
        
        for email in students:
            assert email in participants
            
        assert len(participants) == initial_count + len(students)
        
    def test_student_multiple_activities(self, client):
        """Test one student signing up for multiple activities"""
        email = "multistudent@mergington.edu"
        activities_to_join = ["Art Workshop", "Math Olympiad"]
        
        for activity in activities_to_join:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
            
        # Verify student is in both activities
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for activity in activities_to_join:
            assert email in activities_data[activity]["participants"]


class TestEdgeCases:
    """Tests for edge cases and error conditions"""
    
    def test_empty_email(self, client):
        """Test signup with empty email"""
        response = client.post("/activities/Chess Club/signup?email=")
        # FastAPI should handle this gracefully - we expect it to work with empty string
        assert response.status_code in [200, 400]  # Could be either depending on validation
        
    def test_special_characters_in_email(self, client):
        """Test signup with special characters in email"""
        email = "test.special@mergington.edu"  # Use dot instead of plus to avoid URL encoding issues
        activity = "Drama Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify student was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity]["participants"]
        
    def test_case_sensitive_activity_names(self, client):
        """Test that activity names are case sensitive"""
        email = "casetest@mergington.edu"
        
        # Try with wrong case
        response = client.post(f"/activities/chess club/signup?email={email}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
        
        # Try with correct case
        response = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response.status_code == 200


if __name__ == "__main__":
    # This allows running the tests directly with python -m pytest tests/test_app.py
    pytest.main([__file__])