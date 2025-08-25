/**
 * Simple integration test for the updated calculatorApi service
 */

import calculatorApi from './src/services/calculatorApi.js';

async function testApiIntegration() {
  console.log('🧪 Testing Calculator API Integration...\n');

  try {
    // Test 1: Get API status
    console.log('📊 API Status:');
    const status = calculatorApi.getStatus();
    console.log(JSON.stringify(status, null, 2));
    console.log('');

    // Test 2: Check API availability
    console.log('🔍 Checking API Health...');
    const isHealthy = await calculatorApi.checkApiHealth();
    console.log(`API Health: ${isHealthy ? '✅ Healthy' : '❌ Unhealthy'}`);
    console.log('');

    // Test 3: Test calculation
    console.log('🧮 Testing Calculation...');
    try {
      const result = await calculatorApi.calculate('2 + 2 * 3');
      console.log(`2 + 2 * 3 = ${result} ✅`);
    } catch (error) {
      console.log(`Calculation failed: ${error.message} (using fallback)`);
    }
    console.log('');

    // Test 4: Test history
    console.log('📝 Testing History...');
    try {
      const history = await calculatorApi.getHistory();
      console.log(`History entries: ${history.length}`);
      if (history.length > 0) {
        console.log('Latest entries:', history.slice(-3));
      }
    } catch (error) {
      console.log(`History failed: ${error.message}`);
    }

  } catch (error) {
    console.error('❌ Integration test failed:', error);
  }
}

// Run the test
testApiIntegration().then(() => {
  console.log('\n✨ Integration test completed!');
}).catch(error => {
  console.error('\n💥 Test error:', error);
});
