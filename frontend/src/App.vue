<!-- src/App.vue -->
<template>
  <div id="app">
    <header class="header">
      <h1>🏠 Banglore House Price Predictor</h1>
      <p>Get instant price estimates for properties in your area</p>
    </header>

    <main class="main-content">
      <div class="container">
        <!-- Debug info -->
        <div class="debug-state" v-if="showDebug">
          <pre>Prediction: {{ prediction }}</pre>
          <pre>Input Data: {{ inputData }}</pre>
        </div>

        <!-- Show form when no prediction exists -->
        <div v-if="!prediction">
          <PredictionForm @prediction="handlePrediction" />
        </div>
        
        <!-- Show result when prediction exists -->
        <div v-else>
          <ResultDisplay 
            :prediction="prediction" 
            :inputData="inputData"
            @reset="resetForm"
          />
        </div>

        <div class="status-indicator" :class="backendStatus">
          Backend: {{ backendStatus === 'connected' ? 'Connected' : 'Disconnected' }}
        </div>
        
        <button @click="showDebug = !showDebug" class="debug-toggle">
          {{ showDebug ? 'Hide Debug' : 'Show Debug' }}
        </button>
      </div>
    </main>

    <footer class="footer">
      <p>Powered by ML Model • Built with FastAPI & Vue.js</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import PredictionForm from './components/PredictionForm.vue';
import ResultDisplay from './components/ResultDisplay.vue';
import api from './services/api';

const prediction = ref(null);
const inputData = ref({});
const backendStatus = ref('checking');
const showDebug = ref(true); // Start with debug enabled

// FIX: Handle the event properly
const handlePrediction = (eventData) => {
  console.log('App.vue received event:', eventData);
  
  // Check if eventData has the prediction directly or nested
  if (eventData.prediction) {
    // New format: { prediction: {...}, formData: {...} }
    prediction.value = eventData.prediction;
    inputData.value = eventData.formData;
  } else if (eventData.estimated_price !== undefined) {
    // Old format: direct prediction object
    prediction.value = eventData;
    inputData.value = eventData.formData || {};
  }
  
  console.log('Prediction set to:', prediction.value);
  console.log('Input data set to:', inputData.value);
};

const resetForm = () => {
  console.log('Resetting form...');
  prediction.value = null;
  inputData.value = {};
};

const checkBackend = async () => {
  try {
    await api.healthCheck();
    backendStatus.value = 'connected';
  } catch (error) {
    backendStatus.value = 'disconnected';
  }
};

onMounted(() => {
  console.log('App.vue mounted');
  checkBackend();
  setInterval(checkBackend, 30000);
});
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  text-align: center;
  padding: 2rem;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.main-content {
  flex: 1;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  width: 100%;
  max-width: 600px;
}

.debug-state {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.75rem;
}

.debug-state pre {
  margin: 0.5rem 0;
}

.status-indicator {
  position: fixed;
  bottom: 100px;
  right: 20px;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  z-index: 100;
}

.status-indicator.connected {
  background-color: #4CAF50;
  color: white;
}

.status-indicator.disconnected {
  background-color: #f44336;
  color: white;
}

.debug-toggle {
  position: fixed;
  bottom: 50px;
  right: 20px;
  padding: 0.5rem 1rem;
  background: #666;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  z-index: 100;
}

.footer {
  text-align: center;
  padding: 1rem;
  background: #2c3e50;
  color: white;
  margin-top: auto;
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .header, .footer {
    padding: 1rem;
  }
  
  .status-indicator,
  .debug-toggle {
    position: static;
    margin-top: 1rem;
    display: block;
    width: 100%;
  }
}
</style>