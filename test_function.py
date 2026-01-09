import json
from unittest.mock import Mock

# Import your main function
from main import main

def create_mock_context(user_id):
    """Create a mock context object that simulates Appwrite's context"""
    context = Mock()
    
    # Mock request body
    context.req.body = json.dumps({"$id": user_id})
    
    # Mock response
    response_data = {}
    def mock_json(data):
        response_data.update(data)
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    
    context.res.json = mock_json
    
    # Mock logger
    def mock_log(msg):
        print(f"[LOG]: {msg}")
    
    context.log = mock_log
    
    return context, response_data

# Test cases
def test_function():
    print("=" * 50)
    print("Testing Appwrite Function")
    print("=" * 50)
    
    # Replace with actual user ID from your Appwrite project
    test_user_id = "695c7e392942d4130ee5"
    
    context, response = create_mock_context(test_user_id)
    
    try:
        result = main(context)
        print("\n✓ Function executed successfully")
        return result
    except Exception as e:
        print(f"\n✗ Function failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_function()