<!-- Update only the location field section in PredictionForm.vue -->
<template>
  <div class="prediction-form">
    <h2>House Price Prediction</h2>
    
    <form @submit.prevent="handleSubmit" class="form">
      <!-- Replace the old location select with searchable dropdown -->
      <div class="form-group">
        <SearchableDropdown
          id="location"
          label="Location"
          v-model="formData.location"
          :options="locations"
          placeholder="Start typing location (e.g., 'JP Nagar', 'Whitefield')"
          :required="true"
          :error="errors.location"
          :helperText="`${locations.length} locations available`"
          @search="handleLocationSearch"
          @select="handleLocationSelect"
        />
      </div>

      <!-- Keep other form fields as is -->
      <div class="form-group">
        <label for="sqft">Square Feet:</label>
        <input 
          id="sqft" 
          type="number" 
          v-model.number="formData.sqft"
          min="100"
          step="50"
          required
        >
        <div v-if="errors.sqft" class="error">{{ errors.sqft }}</div>
      </div>

      <div class="form-group">
        <label for="bhk">BHK:</label>
        <input 
          id="bhk" 
          type="number" 
          v-model.number="formData.bhk"
          min="1"
          max="10"
          required
        >
        <div v-if="errors.bhk" class="error">{{ errors.bhk }}</div>
      </div>

      <div class="form-group">
        <label for="bath">Bathrooms:</label>
        <input 
          id="bath" 
          type="number" 
          v-model.number="formData.bath"
          min="1"
          max="10"
          required
        >
        <div v-if="errors.bath" class="error">{{ errors.bath }}</div>
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Predicting...' : 'Predict Price' }}
      </button>
    </form>

    <!-- Add search tips -->
    <div class="search-tips" v-if="locations.length > 0">
      <h4>💡 Search Tips:</h4>
      <ul>
        <li>Type partial names like "jpn" for "JP Nagar"</li>
        <li>Use abbreviations like "kr pu" for "KR Puram"</li>
        <li>Try different spellings if you don't find exact match</li>
        <li>Recent searches are saved for quick access</li>
      </ul>
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, defineEmits, onMounted } from 'vue';
import api from '../services/api';
import SearchableDropdown from './SearchableDropdown.vue'; // Import the new component

const emit = defineEmits(['prediction']);

const formData = reactive({
  location: '',
  sqft: 1000,
  bhk: 2,
  bath: 2
});

const locations = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');
const errors = reactive({});

// Add these new functions
const handleLocationSearch = (searchTerm) => {
  console.log('Searching for:', searchTerm);
  // You could add debounced API search here if needed
};

const handleLocationSelect = (selectedLocation) => {
  console.log('Selected location:', selectedLocation);
  formData.location = selectedLocation;
};

const loadLocations = async () => {
  try {
    locations.value = await api.getLocations();
    console.log(`Loaded ${locations.value.length} locations`);
    
    // Sort locations alphabetically for better search
    locations.value.sort();
    
  } catch (error) {
    errorMessage.value = 'Failed to load locations. Please check if backend is running.';
    console.error('Location loading error:', error);
  }
};

// Keep other functions the same...
const validateForm = () => {
  let isValid = true;
  errors.location = '';
  errors.sqft = '';
  errors.bhk = '';
  errors.bath = '';

  if (!formData.location) {
    errors.location = 'Location is required';
    isValid = false;
  }

  if (formData.sqft < 100) {
    errors.sqft = 'Square feet must be at least 100';
    isValid = false;
  }

  if (formData.bhk < 1 || formData.bhk > 10) {
    errors.bhk = 'BHK must be between 1 and 10';
    isValid = false;
  }

  if (formData.bath < 1 || formData.bath > 10) {
    errors.bath = 'Bathrooms must be between 1 and 10';
    isValid = false;
  }

  return isValid;
};

const handleSubmit = async () => {
  console.log('Form submitted with:', formData);
  
  if (!validateForm()) {
    console.log('Form validation failed');
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    console.log('Calling predictPrice API...');
    const prediction = await api.predictPrice(formData);
    console.log('API response:', prediction);
    
    emit('prediction', {
      prediction: prediction,
      formData: { ...formData }
    });
    
  } catch (error) {
    console.error('API Error:', error);
    errorMessage.value = `Prediction failed: ${error.message}`;
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  console.log('PredictionForm mounted');
  loadLocations();
});
</script>

<style scoped>
.prediction-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: #333;
}

input, select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus, select:focus {
  outline: none;
  border-color: #4CAF50;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: #f44336;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #ffebee;
  border: 1px solid #f44336;
  border-radius: 4px;
  color: #f44336;
}

.search-tips {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #4CAF50;
}

.search-tips h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #333;
}

.search-tips ul {
  margin: 0;
  padding-left: 1.25rem;
  color: #666;
}

.search-tips li {
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}
</style>