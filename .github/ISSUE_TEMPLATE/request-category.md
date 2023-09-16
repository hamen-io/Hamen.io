---
name: Category Request
about: Propose a New Category for Guides, Blogs, Quizzes, or Software
title: "[CATEGORY REQUEST]"
labels: enhancement
assignees: ''

---

**Description:**
Please provide detailed information regarding your proposed category below.

**Category Details:**

- **Subpage Selection:** 
  - id: subpage
  - type: dropdown
  - attributes:
    - label: Select the Target Subpage for Your Category Request
    - options:
      - Documentation (Inclusive of "Blogs" & "Quizzes")
      - Documentation/Blogs
      - Documentation/Guides
      - Quizzes
      - Software
    - validations:
      - required: true

- **Category Title:** 
  - id: category-title
  - type: input
  - label: Enter a Descriptive Category Title
    - placeholder: E.g., "Advanced AI Algorithms" 
    - validations:
      - required: true

- **Additional Information:**
  - type: textarea
  - label: Provide Supplementary Information
    - placeholder: Describe the intended purpose, scope, and potential content of this category. Offer examples of potential articles, blogs, guides, or quizzes that may be featured.

**Guidelines:**
Please ensure that your category request is clear, well-structured, and aligns with the purpose of our platform. The proposed category should contribute positively to our content diversity and user experience.

Your cooperation in providing detailed information is greatly appreciated. Thank you for your contribution!
