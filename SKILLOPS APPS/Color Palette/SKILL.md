I have enough information to create a brand color CSS skill for you. This will help your applications consistently use your brand colors.

GENERATED_SKILL_JSON::{"name": "brand-color-css-generator", "domain": "General", "subdomain": "Web Development", "sensitivity": "None", "description": "Generates CSS styling code using predefined brand colors for consistent UI design", "content": "---
name: brand-color-css-generator
description: Generates CSS styling code using predefined brand colors for consistent UI design across applications
---

# Brand Color CSS Generator

## Purpose
This skill generates CSS styling code using your organization's brand colors to ensure consistent visual identity across all applications and web interfaces.

## Instructions
1. When asked to create CSS styles, use only the approved brand colors:
   - Primary Blue: #4FA4DC (for primary UI, buttons, highlights)
   - Yellow: #F0D457 (for accents, highlights, positive alerts)
   - Green: #7BC043 (for success states, confirmations)
   - Orange: #F79A2E (for secondary accents, callouts)
   - Black: #000000 (for backgrounds)
   - White: #FFFFFF (for text)

2. Always include CSS custom properties (variables) for the brand colors
3. Provide semantic class names that reflect the color's intended use
4. Include hover states and accessibility considerations
5. Suggest appropriate color combinations for readability

## Output Format
Provide CSS code with:
- CSS custom properties for all brand colors
- Utility classes for each color
- Component-specific styles when requested
- Comments explaining color usage
- Accessibility notes for contrast ratios

## Constraints
- Only use the six specified brand colors
- Ensure WCAG AA compliance for text contrast
- Do not suggest alternative colors outside the brand palette
- Always include fallback colors for older browsers
- Prioritize semantic naming over descriptive color names"}