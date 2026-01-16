<!-- src/components/ResultDisplay.vue -->
<template>
  <div class="result-display" v-if="prediction">
    <div class="result-card">
      <h3>Prediction Result</h3>
      
      <div class="result-details">
        <div class="result-item">
          <span class="label">Estimated Price:</span>
          <span class="value price">
            {{ formatLakhsToIndianPrice(prediction.estimated_price) }}
            <span class="price-unit">{{ getPriceUnitFromLakhs(prediction.estimated_price) }}</span>
          </span>
        </div>
        
        <!-- Model output explanation -->
        <div class="model-output-info">
          <p><strong>Model Output:</strong> {{ prediction.estimated_price }} lakhs</p>
          <small class="explanation-note">(Note: Model returns price in lakhs of rupees)</small>
        </div>
        
        <div v-if="inputData && Object.keys(inputData).length > 0" class="input-summary">
          <h4>Input Summary</h4>
          <div class="summary-item">
            <span>Location:</span>
            <span>{{ inputData.location || 'N/A' }}</span>
          </div>
          <div class="summary-item">
            <span>Square Feet:</span>
            <span>{{ (inputData.sqft || 0).toLocaleString() }} sqft</span>
          </div>
          <div class="summary-item">
            <span>BHK:</span>
            <span>{{ inputData.bhk || 'N/A' }}</span>
          </div>
          <div class="summary-item">
            <span>Bathrooms:</span>
            <span>{{ inputData.bath || 'N/A' }}</span>
          </div>
        </div>
        
        <div v-else class="no-input-data">
          <p>No input data available</p>
        </div>
      </div>
      
      <div class="price-breakdown" v-if="prediction.estimated_price">
        <h4>💰 Price Breakdown</h4>
        <div class="breakdown-grid">
          <div class="breakdown-item">
            <span class="breakdown-label">In Crores:</span>
            <span class="breakdown-value">{{ getCroresFromLakhs(prediction.estimated_price) }}</span>
          </div>
          <div class="breakdown-item">
            <span class="breakdown-label">In Lakhs:</span>
            <span class="breakdown-value">{{ getLakhsFromLakhs(prediction.estimated_price) }}</span>
          </div>
          <div class="breakdown-item">
            <span class="breakdown-label">In Thousands:</span>
            <span class="breakdown-value">{{ getThousandsFromLakhs(prediction.estimated_price) }}</span>
          </div>
          <div class="breakdown-item">
            <span class="breakdown-label">Total Rupees:</span>
            <span class="breakdown-value">{{ getTotalRupees(prediction.estimated_price) }}</span>
          </div>
        </div>
      </div>
      
      <button @click="$emit('reset')" class="reset-btn">
        Make Another Prediction
      </button>
      
      <!-- Debug info -->
      <div class="result-debug" v-if="showResultDebug">
        <pre>Raw Model Output: {{ prediction.estimated_price }} lakhs</pre>
        <pre>Input Data Object: {{ inputData }}</pre>
      </div>
    </div>
  </div>
  
  <div v-else class="no-prediction">
    <p>No prediction data available</p>
    <button @click="$emit('reset')" class="reset-btn">
      Try Again
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';

defineProps({
  prediction: {
    type: [Object, String, Number],
    default: null
  },
  inputData: {
    type: Object,
    default: () => ({})
  }
});

defineEmits(['reset']);

const showResultDebug = ref(true);

// Convert model output (in lakhs) to Indian price format
const formatLakhsToIndianPrice = (priceInLakhs) => {
  if (!priceInLakhs && priceInLakhs !== 0) return 'N/A';
  
  if (typeof priceInLakhs !== 'number') {
    priceInLakhs = parseFloat(priceInLakhs);
    if (isNaN(priceInLakhs)) return priceInLakhs;
  }
  
  // If price is 100 lakhs or more, show in crores
  if (priceInLakhs >= 100) {
    const crores = priceInLakhs / 100;
    return crores.toFixed(2);
  } 
  // If price is less than 100 lakhs, show in lakhs with decimal
  else if (priceInLakhs >= 1) {
    return priceInLakhs.toFixed(2);
  }
  // If price is less than 1 lakh, show in thousands
  else {
    const thousands = priceInLakhs * 100;
    return thousands.toFixed(0);
  }
};

// Get appropriate unit based on lakhs value
const getPriceUnitFromLakhs = (priceInLakhs) => {
  if (!priceInLakhs && priceInLakhs !== 0) return '';
  
  if (typeof priceInLakhs !== 'number') {
    priceInLakhs = parseFloat(priceInLakhs);
    if (isNaN(priceInLakhs)) return '';
  }
  
  if (priceInLakhs >= 100) {
    return 'Crores';
  } else if (priceInLakhs >= 1) {
    return 'Lakhs';
  } else {
    return 'Thousands';
  }
};

// Get crores breakdown
const getCroresFromLakhs = (priceInLakhs) => {
  if (!priceInLakhs && priceInLakhs !== 0) return 'N/A';
  
  if (typeof priceInLakhs !== 'number') {
    priceInLakhs = parseFloat(priceInLakhs);
    if (isNaN(priceInLakhs)) return 'N/A';
  }
  
  const crores = Math.floor(priceInLakhs / 100);
  const remainingLakhs = priceInLakhs % 100;
  
  if (crores > 0) {
    if (remainingLakhs > 0) {
      return `${crores} crore ${remainingLakhs.toFixed(2)} lakh`;
    } else {
      return `${crores} crore`;
    }
  } else {
    return '0 crore';
  }
};

// Get lakhs breakdown
const getLakhsFromLakhs = (priceInLakhs) => {
  if (!priceInLakhs && priceInLakhs !== 0) return 'N/A';
  
  if (typeof priceInLakhs !== 'number') {
    priceInLakhs = parseFloat(priceInLakhs);
    if (isNaN(priceInLakhs)) return 'N/A';
  }
  
  const lakhs = Math.floor(priceInLakhs);
  const decimalPart = priceInLakhs - lakhs;
  
  if (decimalPart > 0) {
    return `${lakhs} lakh ${(decimalPart * 100).toFixed(0)} thousand`;
  } else {
    return `${lakhs} lakh`;
  }
};

// Get thousands breakdown
const getThousandsFromLakhs = (priceInLakhs) => {
  if (!priceInLakhs && priceInLakhs !== 0) return 'N/A';
  
  if (typeof priceInLakhs !== 'number') {
    priceInLakhs = parseFloat(priceInLakhs);
    if (isNaN(priceInLakhs)) return 'N/A';
  }
  
  const totalThousands = priceInLakhs * 100;
  return new Intl.NumberFormat('en-IN').format(totalThousands.toFixed(0)) + ' thousand';
};

// Get total rupees
const getTotalRupees = (priceInLakhs) => {
  if (!priceInLakhs && priceInLakhs !== 0) return 'N/A';
  
  if (typeof priceInLakhs !== 'number') {
    priceInLakhs = parseFloat(priceInLakhs);
    if (isNaN(priceInLakhs)) return 'N/A';
  }
  
  const totalRupees = priceInLakhs * 100000;
  return '₹' + new Intl.NumberFormat('en-IN').format(totalRupees.toFixed(0));
};

// Get price interpretation
const getPriceInterpretation = (priceInLakhs) => {
  if (!priceInLakhs && priceInLakhs !== 0) return '';
  
  if (typeof priceInLakhs !== 'number') {
    priceInLakhs = parseFloat(priceInLakhs);
    if (isNaN(priceInLakhs)) return '';
  }
  
  if (priceInLakhs >= 100) {
    const crores = priceInLakhs / 100;
    return `This is equivalent to ${crores.toFixed(2)} crores (${priceInLakhs.toFixed(2)} lakhs)`;
  } else if (priceInLakhs >= 1) {
    return `This is equivalent to ${priceInLakhs.toFixed(2)} lakhs`;
  } else {
    const thousands = priceInLakhs * 100;
    return `This is equivalent to ${thousands.toFixed(0)} thousands`;
  }
};
</script>

<style scoped>
.result-display {
  margin-top: 2rem;
}

.result-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.result-details {
  margin: 1.5rem 0;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.label {
  font-size: 1.1rem;
  opacity: 0.9;
}

.price {
  font-size: 2.5rem;
  font-weight: bold;
  color: #ffd700;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
}

.price-unit {
  font-size: 1rem;
  color: #ffeb3b;
  margin-top: 0.25rem;
  font-weight: normal;
}

.model-output-info {
  background: rgba(255, 255, 255, 0.15);
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  border-left: 3px solid #4CAF50;
}

.model-output-info p {
  margin: 0 0 0.25rem 0;
  font-weight: 500;
}

.explanation-note {
  opacity: 0.8;
  font-size: 0.85rem;
}

.input-summary {
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1.5rem;
}

.input-summary h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #ffd700;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-item:last-child {
  border-bottom: none;
}

.price-breakdown {
  background: rgba(255, 255, 255, 0.15);
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.price-breakdown h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #ffd700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breakdown-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.breakdown-item {
  display: flex;
  flex-direction: column;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
}

.breakdown-label {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 0.25rem;
}

.breakdown-value {
  font-weight: bold;
  color: #ffd700;
}

.no-input-data {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
  opacity: 0.8;
}

.no-prediction {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.reset-btn {
  width: 100%;
  padding: 0.75rem;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 1.5rem;
}

.reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.result-debug {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.75rem;
  max-height: 200px;
  overflow-y: auto;
}

.result-debug pre {
  margin: 0.5rem 0;
  white-space: pre-wrap;
}

/* Responsive */
@media (max-width: 768px) {
  .breakdown-grid {
    grid-template-columns: 1fr;
  }
  
  .price {
    font-size: 2rem;
  }
}
</style>