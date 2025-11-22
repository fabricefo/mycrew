#!/usr/bin/env python3
"""
Test script for PexelsCoverImageTool
Run this to verify the tool works before integrating with CrewAI
"""

import os
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your tool (adjust path as needed)
try:
    from tools.image_search_tool import PexelsCoverImageTool
except ImportError:
    print("Could not import PexelsCoverImageTool. Make sure the path is correct.")
    sys.exit(1)

def test_topic_search():
    """Test 1: Search by specific topic"""
    print("=" * 50)
    print("TEST 1: Topic-specific search")
    print("=" * 50)
    
    tool = PexelsCoverImageTool()
    topic = "google deepmind random images"
    
    print(f"Searching for: {topic}")
    result_json = tool._run(topic=topic, attempts=1)
    result = json.loads(result_json)
    
    if result.get('success'):
        cover_image = result['cover_image']
        print("✅ SUCCESS - Found cover image:")
        print(f"   URL: {cover_image['cover_url']}")
        print(f"   Dimensions: {cover_image['dimensions']['width']}x{cover_image['dimensions']['height']}")
        print(f"   Photographer: {cover_image['photographer']}")
        print(f"   SizeOptimized: {cover_image['size_optimized']}")
        print(f"   Search Query: {cover_image['search_query']}")
    else:
        print("❌ FAILED - No suitable image found")
        print(f"   Error: {result.get('error')}")
    
    return result.get('success', False)

def test_fallback_search():
    """Test 2: Test fallback mechanism with 2 attempts"""
    print("\n" + "=" * 50)
    print("TEST 2: Fallback search (2 attempts)")
    print("=" * 50)
    
    tool = PexelsCoverImageTool()
    topic = "very-specific-nonexistent-topic-12345"  # This should fail and fallback
    
    print(f"Searching for: {topic} (should fallback to tech images)")
    result_json = tool._run(topic=topic, attempts=2)
    result = json.loads(result_json)
    
    if result.get('success'):
        cover_image = result['cover_image']
        print("✅ SUCCESS - Found fallback cover image:")
        print(f"   URL: {cover_image['cover_url']}")
        print(f"   Dimensions: {cover_image['dimensions']['width']}x{cover_image['dimensions']['height']}")
        print(f"   Photographer: {cover_image['photographer']}")
        print(f"   Search Query Used: {cover_image['search_query']}")
        print(f"   Message: {result['message']}")
    else:
        print("❌ FAILED - Even fallback failed")
        print(f"   Error: {result.get('error')}")
        print(f"   Attempts Made: {result.get('attempts_made', [])}")
    
    return result.get('success', False)

def test_common_topics():
    """Test 3: Test several common tech topics"""
    print("\n" + "=" * 50)
    print("TEST 3: Common tech topics")
    print("=" * 50)
    
    topics = [
        "artificial intelligence",
        "machine learning", 
        "programming",
        "software development",
        "technology"
    ]
    
    tool = PexelsCoverImageTool()
    successes = 0
    
    for topic in topics:
        print(f"\nTesting: {topic}")
        result_json = tool._run(topic=topic, attempts=1)
        result = json.loads(result_json)
        
        if result.get('success'):
            print(f"✅ Found image - {result['cover_image']['dimensions']['width']}x{result['cover_image']['dimensions']['height']}")
            successes += 1
        else:
            print(f"❌ Failed - {result.get('error', 'Unknown error')}")
    
    print(f"\nSuccess rate: {successes}/{len(topics)} ({successes/len(topics)*100:.1f}%)")
    return successes == len(topics)

def test_api_key():
    """Test 4: Verify API key is working"""
    print("\n" + "=" * 50)
    print("TEST 4: API Key verification")
    print("=" * 50)
    
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print("❌ PEXELS_API_KEY not found in environment variables")
        print("   Please set your Pexels API key:")
        print("   export PEXELS_API_KEY='your_actual_api_key_here'")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        tool = PexelsCoverImageTool()
        print("✅ Tool initialized successfully")
        return True
    except ValueError as e:
        print(f"❌ Tool initialization failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("PEXELS COVER IMAGE TOOL - TEST SUITE")
    print("=" * 60)
    
    # Test results
    results = []
    
    # Test API key first
    results.append(("API Key Check", test_api_key()))
    
    if not results[0][1]:  # If API key test failed, don't run other tests
        print("\n❌ Cannot proceed without valid API key")
        return
    
    # Run other tests
    results.append(("Topic Search", test_topic_search()))
    results.append(("Fallback Search", test_fallback_search()))
    results.append(("Common Topics", test_common_topics()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your tool is ready to integrate with CrewAI.")
    else:
        print(f"\n⚠️  {len(results)-passed} test(s) failed. Please fix issues before using with CrewAI.")

if __name__ == "__main__":
    run_all_tests()