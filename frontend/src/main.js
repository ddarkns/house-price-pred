// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import SearchableDropdown from './components/SearchableDropdown.vue';

const app = createApp(App);
app.component('SearchableDropdown', SearchableDropdown);
app.mount('#app');