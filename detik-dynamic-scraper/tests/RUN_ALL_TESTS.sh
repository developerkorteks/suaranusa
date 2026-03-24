#!/bin/bash
# Run all tests in sequence

echo "🧪 Running All Tests - Detik Dynamic Scraper"
echo "=" | tr '=' '=' | head -c 70 && echo

source ../venv_detik/bin/activate

echo -e "\n1️⃣ Testing Domain Discovery (Step 1)..."
python3 test_quick.py || exit 1

echo -e "\n2️⃣ Testing Endpoint Detection (Step 2)..."
python3 test_step2.py || exit 1

echo -e "\n3️⃣ Testing Parameter Extraction (Step 3)..."
python3 test_step3.py || exit 1

echo -e "\n4️⃣ Testing Content Scraper (Step 4)..."
timeout 60 python3 test_step4.py || exit 1

echo -e "\n5️⃣ Testing Data Normalizer (Step 5)..."
python3 test_step5.py || exit 1

echo -e "\n6️⃣ Testing Storage Layer (Step 6)..."
python3 test_step6.py || exit 1

echo -e "\n7️⃣ Testing REST API (Step 7)..."
timeout 45 python3 test_step7.py || exit 1

echo -e "\n8️⃣ Running Integration Test..."
timeout 90 python3 test_integration.py || exit 1

echo -e "\n" && echo "=" | tr '=' '=' | head -c 70 && echo
echo "✅ ALL TESTS PASSED!"
echo "🎉 System is production ready!"
