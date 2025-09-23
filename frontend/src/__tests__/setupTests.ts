import '@testing-library/jest-dom';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock as any;

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  disconnect: jest.fn(),
  unobserve: jest.fn(),
  root: null,
  rootMargin: '',
  thresholds: [],
  takeRecords: jest.fn(),
})) as any;

// Mock HTML5 drag and drop APIs
Object.defineProperty(window, 'DataTransfer', {
  writable: true,
  value: class DataTransfer {
    data: { [key: string]: string } = {};
    
    setData(format: string, data: string) {
      this.data[format] = data;
    }
    
    getData(format: string) {
      return this.data[format] || '';
    }
  }
});

// Mock console.error to suppress error logs during tests unless explicitly expected
const originalError = console.error;
beforeAll(() => {
  console.error = jest.fn();
});

afterAll(() => {
  console.error = originalError;
});

// Reset mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});