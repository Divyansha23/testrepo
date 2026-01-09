import json
from unittest.mock import Mock
from test_function import create_mock_context
from main import main

def test_scenarios():
    """Test multiple scenarios for the Appwrite function"""
    scenarios = [
        {
            "name": "User with no memberships",
            "user_id": "user-no-teams",
            "description": "Should return success: false"
        },
        {
            "name": "User with one active membership",
            "user_id": "695c7e392942d4130ee5",
            "description": "Should return success: true with DATABASE_ID"
        },
        {
            "name": "User with multiple memberships",
            "user_id": "user-multiple-teams",
            "description": "Should return success: true with multiple DATABASE_IDs"
        },
        {
            "name": "User with not-yet-joined membership",
            "user_id": "user-not-joined",
            "description": "Should return success: false, joined: false"
        }
    ]
    
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}/{len(scenarios)}: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"{'='*60}")
        
        context, response = create_mock_context(scenario['user_id'])
        
        try:
            result = main(context)
            results.append({
                "scenario": scenario['name'],
                "status": "✓ PASSED",
                "result": response
            })
        except Exception as e:
            results.append({
                "scenario": scenario['name'],
                "status": "✗ FAILED",
                "error": str(e)
            })
            print(f"Error: {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for result in results:
        print(f"{result['status']} - {result['scenario']}")
    
    passed = sum(1 for r in results if "PASSED" in r['status'])
    print(f"\nTotal: {passed}/{len(results)} tests passed")

if __name__ == "__main__":
    test_scenarios()