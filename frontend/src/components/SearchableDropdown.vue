<!-- src/components/SearchableDropdown.vue -->
<template>
  <div class="searchable-dropdown">
    <div class="dropdown-header">
      <label :for="id" v-if="label">{{ label }}</label>
      <span class="required-indicator" v-if="required">*</span>
    </div>
    
    <div class="dropdown-container" :class="{ 'is-focused': isFocused, 'has-error': error }">
      <!-- Input with dropdown icon -->
      <div class="input-wrapper">
        <input
          :id="id"
          ref="inputRef"
          :type="type"
          :value="searchQuery"
          @input="handleInput"
          @focus="onFocus"
          @blur="onBlur"
          @keydown.enter="handleEnter"
          @keydown.down="moveDown"
          @keydown.up="moveUp"
          :placeholder="placeholder"
          :disabled="disabled"
          :required="required"
          class="dropdown-input"
          autocomplete="off"
        />
        
        <!-- Dropdown icon -->
        <div class="dropdown-icon" @click="toggleDropdown">
          <svg v-if="isDropdownOpen" width="20" height="20" viewBox="0 0 24 24">
            <path fill="currentColor" d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z"/>
          </svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24">
            <path fill="currentColor" d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
          </svg>
        </div>
      </div>
      
      <!-- Error message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <!-- Helper text -->
      <div v-if="helperText" class="helper-text">
        {{ helperText }}
      </div>
      
      <!-- Dropdown menu -->
      <div 
        v-if="isDropdownOpen && filteredOptions.length > 0" 
        class="dropdown-menu"
        ref="dropdownMenuRef"
      >
        <div class="dropdown-content">
          <!-- Recent searches section -->
          <div v-if="recentSearches.length > 0" class="dropdown-section">
            <div class="section-header">
              <span class="section-title">Recent Searches</span>
              <button 
                v-if="recentSearches.length > 0"
                @click="clearRecentSearches" 
                class="clear-button"
              >
                Clear
              </button>
            </div>
            <div 
              v-for="(item, index) in recentSearches" 
              :key="'recent-' + index"
              class="dropdown-item recent-item"
              :class="{ 'is-active': activeIndex === -index - 1 }"
              @mousedown="selectRecent(item)"
            >
              <div class="item-content">
                <span class="item-text">{{ item }}</span>
                <span class="recent-badge">Recent</span>
              </div>
            </div>
          </div>
          
          <!-- Search results section -->
          <div class="dropdown-section">
            <div class="section-header">
              <span class="section-title">Suggestions</span>
              <span class="results-count">{{ filteredOptions.length }} found</span>
            </div>
            
            <!-- No results message -->
            <div v-if="filteredOptions.length === 0" class="no-results">
              <div class="no-results-icon">🔍</div>
              <div class="no-results-text">No locations found</div>
              <div class="no-results-hint">Try different keywords</div>
            </div>
            
            <!-- Results list -->
            <div 
              v-for="(option, index) in filteredOptions" 
              :key="option"
              class="dropdown-item"
              :class="{ 
                'is-active': activeIndex === index,
                'is-highlighted': isOptionHighlighted(option)
              }"
              @mousedown="selectOption(option)"
            >
              <div class="item-content">
                <!-- Option text with highlighted matches -->
                <span class="item-text" v-html="highlightMatch(option)"></span>
                
                <!-- Match score badge (for debugging/visual feedback) -->
                <span v-if="showMatchScore" class="score-badge">
                  {{ getMatchScore(option).toFixed(2) }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- Quick actions -->
          <div v-if="showQuickActions" class="quick-actions">
            <button @mousedown="selectFirstMatch" class="quick-action-btn">
              Select first match
            </button>
            <button @mousedown="clearSearch" class="quick-action-btn">
              Clear search
            </button>
          </div>
        </div>
      </div>
      
      <!-- Selected value chips (if multiple selection) -->
      <div v-if="selectedValues.length > 0 && multiple" class="selected-chips">
        <div 
          v-for="value in selectedValues" 
          :key="value"
          class="chip"
        >
          {{ value }}
          <button @click="removeChip(value)" class="chip-remove">
            ×
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  id: {
    type: String,
    default: 'searchable-dropdown'
  },
  label: {
    type: String,
    default: ''
  },
  options: {
    type: Array,
    default: () => []
  },
  modelValue: {
    type: [String, Array],
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Type to search...'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  helperText: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  multiple: {
    type: Boolean,
    default: false
  },
  showMatchScore: {
    type: Boolean,
    default: false // For debugging
  },
  showQuickActions: {
    type: Boolean,
    default: true
  },
  fuzzySearch: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['update:modelValue', 'search', 'select', 'clear']);

const inputRef = ref(null);
const dropdownMenuRef = ref(null);
const searchQuery = ref('');
const isDropdownOpen = ref(false);
const isFocused = ref(false);
const activeIndex = ref(-1);
const recentSearches = ref([]);
const selectedValues = ref([]);

// Load recent searches from localStorage
const loadRecentSearches = () => {
  const saved = localStorage.getItem('recent-location-searches');
  if (saved) {
    recentSearches.value = JSON.parse(saved).slice(0, 5); // Keep only 5 most recent
  }
};

// Save recent search
const saveRecentSearch = (value) => {
  if (!value || recentSearches.value.includes(value)) return;
  
  recentSearches.value.unshift(value);
  recentSearches.value = recentSearches.value.slice(0, 5); // Keep only 5 most recent
  localStorage.setItem('recent-location-searches', JSON.stringify(recentSearches.value));
};

// Clear recent searches
const clearRecentSearches = () => {
  recentSearches.value = [];
  localStorage.removeItem('recent-location-searches');
};

// Calculate fuzzy match score
const getMatchScore = (option) => {
  const query = searchQuery.value.toLowerCase();
  const text = option.toLowerCase();
  
  if (!query) return 0;
  
  // Exact match
  if (text === query) return 1.0;
  
  // Starts with query
  if (text.startsWith(query)) return 0.9;
  
  // Contains query
  if (text.includes(query)) return 0.8;
  
  // Fuzzy matching - find characters in order
  let queryIndex = 0;
  for (let i = 0; i < text.length && queryIndex < query.length; i++) {
    if (text[i] === query[queryIndex]) {
      queryIndex++;
    }
  }
  
  // Return score based on how many characters matched in order
  if (queryIndex === query.length) {
    return 0.7 - (text.length - query.length) * 0.01; // Penalize longer strings
  }
  
  // Partial word match (split by spaces/dashes)
  const words = text.split(/[\s\-]+/);
  for (const word of words) {
    if (word.startsWith(query)) return 0.6;
    if (word.includes(query)) return 0.5;
  }
  
  // No match
  return 0;
};

// Highlight matching text
const highlightMatch = (option) => {
  if (!searchQuery.value) return option;
  
  const query = searchQuery.value.toLowerCase();
  const text = option.toLowerCase();
  
  // Find the position where query appears
  const index = text.indexOf(query);
  
  if (index === -1) {
    // For fuzzy matches, highlight characters that match in order
    let highlighted = '';
    let queryIndex = 0;
    
    for (let i = 0; i < option.length; i++) {
      const char = option[i];
      if (queryIndex < query.length && text[i] === query[queryIndex]) {
        highlighted += `<span class="highlight">${char}</span>`;
        queryIndex++;
      } else {
        highlighted += char;
      }
    }
    return highlighted;
  }
  
  // Direct match found
  const before = option.substring(0, index);
  const match = option.substring(index, index + query.length);
  const after = option.substring(index + query.length);
  
  return `${before}<span class="highlight">${match}</span>${after}`;
};

// Check if option is highlighted based on score
const isOptionHighlighted = (option) => {
  return getMatchScore(option) >= 0.8;
};

// Filter and sort options based on search query
const filteredOptions = computed(() => {
  if (!searchQuery.value) {
    return props.options.slice(0, 10); // Show first 10 when no search
  }
  
  const query = searchQuery.value.toLowerCase();
  
  // Calculate scores for all options
  const optionsWithScores = props.options.map(option => ({
    option,
    score: getMatchScore(option)
  }));
  
  // Filter out zero-score options and sort by score
  return optionsWithScores
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .map(item => item.option)
    .slice(0, 15); // Limit to 15 results
});

// Handle input
const handleInput = (event) => {
  searchQuery.value = event.target.value;
  isDropdownOpen.value = true;
  activeIndex.value = -1;
  emit('search', searchQuery.value);
  
  // If not multiple selection, update model value
  if (!props.multiple) {
    emit('update:modelValue', searchQuery.value);
  }
};

// Focus handler
const onFocus = () => {
  isFocused.value = true;
  isDropdownOpen.value = true;
};

// Blur handler with delay to allow click events
const onBlur = () => {
  setTimeout(() => {
    isFocused.value = false;
    isDropdownOpen.value = false;
  }, 200);
};

// Toggle dropdown
const toggleDropdown = () => {
  if (props.disabled) return;
  isDropdownOpen.value = !isDropdownOpen.value;
  if (isDropdownOpen.value) {
    inputRef.value.focus();
  }
};

// Select an option
const selectOption = (option) => {
  if (props.multiple) {
    if (!selectedValues.value.includes(option)) {
      selectedValues.value.push(option);
      emit('update:modelValue', selectedValues.value);
    }
  } else {
    searchQuery.value = option;
    emit('update:modelValue', option);
    isDropdownOpen.value = false;
    saveRecentSearch(option);
  }
  emit('select', option);
  
  // Reset active index
  activeIndex.value = -1;
};

// Select recent search
const selectRecent = (item) => {
  searchQuery.value = item;
  emit('update:modelValue', item);
  isDropdownOpen.value = false;
  emit('select', item);
};

// Clear search
const clearSearch = () => {
  searchQuery.value = '';
  emit('update:modelValue', '');
  emit('clear');
  inputRef.value.focus();
};

// Handle Enter key
const handleEnter = () => {
  if (activeIndex.value >= 0 && filteredOptions.value.length > 0) {
    selectOption(filteredOptions.value[activeIndex.value]);
  } else if (filteredOptions.value.length > 0) {
    selectOption(filteredOptions.value[0]);
  }
  isDropdownOpen.value = false;
};

// Move selection down
const moveDown = (event) => {
  event.preventDefault();
  if (filteredOptions.value.length > 0) {
    activeIndex.value = (activeIndex.value + 1) % filteredOptions.value.length;
    scrollToActiveItem();
  }
};

// Move selection up
const moveUp = (event) => {
  event.preventDefault();
  if (filteredOptions.value.length > 0) {
    activeIndex.value = activeIndex.value <= 0 
      ? filteredOptions.value.length - 1 
      : activeIndex.value - 1;
    scrollToActiveItem();
  }
};

// Scroll to active item in dropdown
const scrollToActiveItem = () => {
  if (dropdownMenuRef.value && activeIndex.value >= 0) {
    const activeElement = dropdownMenuRef.value.querySelector('.is-active');
    if (activeElement) {
      activeElement.scrollIntoView({ block: 'nearest' });
    }
  }
};

// Select first match
const selectFirstMatch = () => {
  if (filteredOptions.value.length > 0) {
    selectOption(filteredOptions.value[0]);
  }
};

// Remove chip (for multiple selection)
const removeChip = (value) => {
  selectedValues.value = selectedValues.value.filter(v => v !== value);
  emit('update:modelValue', selectedValues.value);
};

// Initialize with model value
watch(() => props.modelValue, (newValue) => {
  if (!props.multiple) {
    searchQuery.value = newValue || '';
  } else {
    selectedValues.value = Array.isArray(newValue) ? newValue : [];
  }
}, { immediate: true });

// Click outside to close dropdown
const handleClickOutside = (event) => {
  if (dropdownMenuRef.value && !dropdownMenuRef.value.contains(event.target) &&
      inputRef.value && !inputRef.value.contains(event.target)) {
    isDropdownOpen.value = false;
  }
};

onMounted(() => {
  loadRecentSearches();
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.searchable-dropdown {
  width: 100%;
  position: relative;
}

.dropdown-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.dropdown-header label {
  font-weight: 600;
  color: #333;
  font-size: 0.875rem;
}

.required-indicator {
  color: #f44336;
  margin-left: 0.25rem;
}

.dropdown-container {
  position: relative;
  transition: all 0.3s ease;
}

.dropdown-container.is-focused {
  border-color: #4CAF50;
}

.dropdown-container.has-error {
  border-color: #f44336;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.dropdown-input {
  width: 100%;
  padding: 0.75rem 3rem 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.dropdown-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.dropdown-input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.dropdown-icon {
  position: absolute;
  right: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.dropdown-icon:hover {
  color: #333;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  max-height: 400px;
  overflow-y: auto;
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-content {
  padding: 0.5rem;
}

.dropdown-section {
  margin-bottom: 0.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 0.25rem;
}

.section-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.results-count {
  font-size: 0.75rem;
  color: #666;
}

.clear-button {
  background: none;
  border: none;
  color: #666;
  font-size: 0.75rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.clear-button:hover {
  background: #f5f5f5;
  color: #333;
}

.dropdown-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-radius: 6px;
  margin: 0.125rem 0;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.dropdown-item.is-active {
  background: #e8f5e8;
  border-left-color: #4CAF50;
}

.dropdown-item.is-highlighted {
  background: #fff8e1;
}

.item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-text {
  flex: 1;
}

.item-text :deep(.highlight) {
  background-color: #ffeb3b;
  padding: 0 2px;
  border-radius: 2px;
  font-weight: 600;
}

.recent-item {
  border-left-color: #2196f3;
}

.recent-badge {
  font-size: 0.7rem;
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  margin-left: 0.5rem;
}

.score-badge {
  font-size: 0.7rem;
  background: #f5f5f5;
  color: #666;
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  font-family: monospace;
}

.no-results {
  padding: 2rem 1rem;
  text-align: center;
  color: #666;
}

.no-results-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.no-results-text {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.no-results-hint {
  font-size: 0.875rem;
  opacity: 0.8;
}

.quick-actions {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem;
  border-top: 1px solid #f0f0f0;
  margin-top: 0.5rem;
}

.quick-action-btn {
  flex: 1;
  padding: 0.5rem;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-action-btn:hover {
  background: #e0e0e0;
}

.selected-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.chip {
  display: inline-flex;
  align-items: center;
  background: #e8f5e8;
  color: #2e7d32;
  padding: 0.375rem 0.75rem;
  border-radius: 16px;
  font-size: 0.875rem;
}

.chip-remove {
  background: none;
  border: none;
  color: #2e7d32;
  font-size: 1.25rem;
  cursor: pointer;
  margin-left: 0.5rem;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.chip-remove:hover {
  background: rgba(0, 0, 0, 0.1);
}

.error-message {
  color: #f44336;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.helper-text {
  color: #666;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>