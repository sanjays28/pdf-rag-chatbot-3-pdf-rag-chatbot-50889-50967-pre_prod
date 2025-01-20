// Jest setup file
Object.defineProperty(window, 'TextEncoder', {
  writable: true,
  value: TextEncoder
});
Object.defineProperty(window, 'TextDecoder', {
  writable: true,
  value: TextDecoder
});

// Mock FormData
global.FormData = class FormData {
  constructor() {
    this.data = {};
  }
  append(key, value) {
    this.data[key] = value;
  }
};