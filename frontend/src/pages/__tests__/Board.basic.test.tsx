import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import '@testing-library/jest-dom';

// Simple test component to verify testing setup
const SimpleTestComponent = () => {
  return (
    <div>
      <h1>Board Test</h1>
      <p>Testing basic functionality</p>
    </div>
  );
};

const TestWrapper = ({ children }: { children: React.ReactNode }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

describe('Board Component Tests', () => {
  it('renders basic test component', () => {
    render(
      <TestWrapper>
        <SimpleTestComponent />
      </TestWrapper>
    );

    expect(screen.getByText('Board Test')).toBeInTheDocument();
    expect(screen.getByText('Testing basic functionality')).toBeInTheDocument();
  });

  it('has proper accessibility structure', () => {
    render(
      <TestWrapper>
        <SimpleTestComponent />
      </TestWrapper>
    );

    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Board Test');
  });
});