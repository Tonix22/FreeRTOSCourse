# Doorstop Setup and Usage Guide

Doorstop is an effective tool for managing requirements directly within your version control system, 
especially useful when integrated with Git. Below are detailed steps for installation and basic usage.

## Installation

### Step 1: Install Python

Ensure Python is installed on your system. Doorstop requires Python 3.

### Step 2: Install Doorstop

Install Doorstop using pip, Python’s package installer:

```bash
doorstop-gui
```

```bash
pip install doorstop
doorstop create REQ ./reqs
doorstop add REQ
```
In the editor, write the requirement:

```bash
doorstop publish all
```
Generate an HTML report of your requirements:

```bash
doorstop publish all path/to/output.html
```

# Explanation of YAML Fields

### 1. `active: true`
- **Meaning:** Indicates whether the requirement is currently active.
- **Usage:** 
  - `true`: The requirement is active and should be considered in the project.
  - `false`: The requirement is inactive (e.g., deprecated, on hold).

### 2. `derived: false`
- **Meaning:** Shows whether the requirement is derived from another requirement.
- **Usage:** 
  - `false`: The requirement is original and not derived from another.
  - `true`: The requirement is derived from another higher-level requirement.

### 3. `header: |`
- **Meaning:** This is a header or title for the requirement. The `|` symbol indicates that the content follows on multiple lines (preserved as is).
- **Usage:** 
  - In this example, `SDD` stands for Software Detailed Design, which is the title or section header for this requirement.

### 4. `level: 1.0`
- **Meaning:** Represents the hierarchical level of the requirement.
- **Usage:** 
  - A lower number (e.g., `1.0`) indicates a higher-level requirement.
  - Sub-requirements might have levels like `1.1`, `1.2`, `2.0`, etc., to organize requirements hierarchically.

### 5. `links:`
- **Meaning:** Holds references or links to other documents, websites, or requirements relevant to this requirement.
- **Usage:** 
  - It’s a list (indicated by `-`), and each item is a link. Currently, the link is set to `null`, but typically it would contain URLs or IDs of related requirements.

### 6. `normative: true`
- **Meaning:** Indicates whether the requirement is normative, meaning it must be complied with.
- **Usage:** 
  - `true`: This requirement is mandatory.
  - `false`: The requirement might be informative or optional.

### 7. `ref: ''`
- **Meaning:** A reference identifier for the requirement, often used to trace it back to a specific source or document.
- **Usage:** 
  - Currently empty (`''`), meaning no reference has been assigned. Typically populated with an ID or document reference.

### 8. `reviewed: null`
- **Meaning:** Indicates whether the requirement has been reviewed.
- **Usage:** 
  - `null`: The requirement hasn’t been reviewed yet, or the review status is unknown. 
  - After review, this might be updated with the date of review or reviewer’s name.

### 9. `text: |`
- **Meaning:** Contains the actual text of the requirement.
- **Usage:** 
  - The `|` symbol indicates that the text is a block of multiline text. In this case, it’s describing the requirement to create a Software Detailed Design (SDD) document, suggesting copying from a template.

### Summary
- **`active`, `derived`, `normative`, and `reviewed`:** Status indicators related to the requirement’s lifecycle.
- **`header`, `text`:** Descriptive fields that contain the main content of the requirement.
- **`level`, `links`, and `ref`:** Organizational fields that help structure and relate the requirement to others.
