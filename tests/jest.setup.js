/**
 * Jest setup file - runs before each test file
 */

// Extend expect with additional matchers
import "@testing-library/jest-dom";

// Mock browser globals that might not be available in JSDOM
global.ResizeObserver = class ResizeObserver {
  constructor(callback) {
    this.callback = callback;
  }
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mock for IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor(callback) {
    this.callback = callback;
  }
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mock fetch API
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({}),
    text: () => Promise.resolve(""),
    ok: true,
  })
);

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = String(value);
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    }),
    length: jest.fn(() => Object.keys(store).length),
    key: jest.fn((index) => Object.keys(store)[index] || null),
  };
})();

Object.defineProperty(window, "localStorage", { value: localStorageMock });

// Console error override to fail tests on prop type errors
const originalConsoleError = console.error;
console.error = (...args) => {
  // Fail tests on prop type errors
  if (
    args[0] &&
    typeof args[0] === "string" &&
    args[0].includes("Warning: Failed prop type")
  ) {
    throw new Error(args[0]);
  }
  originalConsoleError(...args);
};

// Reset all mocks after each test
afterEach(() => {
  jest.clearAllMocks();
});
