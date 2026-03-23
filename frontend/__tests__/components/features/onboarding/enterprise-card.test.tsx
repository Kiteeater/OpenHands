import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { EnterpriseCard } from "#/components/features/onboarding/enterprise-card";

describe("EnterpriseCard", () => {
  const defaultProps = {
    icon: <svg data-testid="test-icon" />,
    title: "Test Title",
    description: "Test description",
    features: ["Feature 1", "Feature 2"],
    onLearnMore: vi.fn(),
    learnMoreLabel: "Learn More",
  };

  it("should render the card with title", () => {
    render(<EnterpriseCard {...defaultProps} />);

    expect(screen.getByText("Test Title")).toBeInTheDocument();
  });

  it("should render the description", () => {
    render(<EnterpriseCard {...defaultProps} />);

    expect(screen.getByText("Test description")).toBeInTheDocument();
  });

  it("should render the icon", () => {
    render(<EnterpriseCard {...defaultProps} />);

    expect(screen.getByTestId("test-icon")).toBeInTheDocument();
  });

  it("should render the features", () => {
    render(<EnterpriseCard {...defaultProps} />);

    expect(screen.getByText("Feature 1")).toBeInTheDocument();
    expect(screen.getByText("Feature 2")).toBeInTheDocument();
  });

  it("should render the learn more button with correct label", () => {
    render(<EnterpriseCard {...defaultProps} />);

    const button = screen.getByRole("button", {
      name: "Learn More Test Title",
    });
    expect(button).toBeInTheDocument();
  });

  it("should call onLearnMore when button is clicked", async () => {
    const mockOnLearnMore = vi.fn();
    const user = userEvent.setup();

    render(<EnterpriseCard {...defaultProps} onLearnMore={mockOnLearnMore} />);

    const button = screen.getByRole("button", {
      name: "Learn More Test Title",
    });
    await user.click(button);

    expect(mockOnLearnMore).toHaveBeenCalledTimes(1);
  });

  it("should have correct aria-label on button", () => {
    render(<EnterpriseCard {...defaultProps} />);

    const button = screen.getByRole("button");
    expect(button).toHaveAttribute("aria-label", "Learn More Test Title");
  });
});
