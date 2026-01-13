# **Refactoring Proposal Summary: Pattern-Centric JSON Schema for ADEPT Framework**

## **Overview**

The proposed refactoring transforms the ADEPT framework's JSON schema from a **configuration-centric** to a **pattern-centric** architecture. This change addresses the ambiguous "component_policies" mapping and creates a cleaner separation between reusable architectural pattern definitions and specific experimental instantiations.

## **Key Problems Identified**

1. **Ambiguous Terminology**: The term "policy" was overloaded to mean both architectural decisions and experimental configurations
2. **Incomplete Bindings**: Policies lacked explicit parameter value bindings
3. **Fragmented Definitions**: Policy definitions were split between pattern and dataspace sections
4. **Limited Reusability**: Pattern definitions couldn't stand alone as reusable architectural templates

## **Core Changes**

### **1. Self-Contained Pattern Definitions**
- **Before**: Patterns defined parameters but policies were incomplete
- **After**: Each pattern includes complete policy definitions with explicit parameter bindings
- **Benefit**: Patterns become standalone, reusable architectural templates

### **2. Clear Separation of Concerns**
```
NEW STRUCTURE:
├── system/                          # PATTERN DEFINITIONS
│   └── components/                  # Reusable architectural templates
│       └── pattern_name/
│           ├── parameters/          # Full specification
│           └── decisions/
│               └── policy_name/     # With complete parameter bindings
├── experiment_design/               # EXPERIMENT CONFIGURATION
│   ├── selected_policies/           # Which policies to test
│   └── scenarios/                   # How to sample uncertainties
└── dataspace/                       # DATA MAPPING
    └── configuration_identification/ # References to pattern policies
```

### **3. Explicit Policy-Parameter Bindings**
- **Added**: `parameter_bindings` field in each policy
- **Contains**: Actual lever values and constraint settings
- **Result**: No ambiguity about what each policy means

### **4. Reference-Based Data Mapping**
- **Changed**: `component_policies` (mapping) → `pattern_policy_references` (references)
- **Benefit**: Data configurations point to pattern definitions without duplicating information

## **Benefits of the New Approach**

### **For Pattern Reusability**
- Patterns can be published as standalone architectural templates
- Multiple experiments can reuse the same pattern with different configurations
- Patterns can be versioned and evolved independently

### **For Analysis Traceability**
- Clear lineage from data rows back to architectural decisions
- Explicit mapping of experimental configurations to pattern policies
- Easier comparison of different policy implementations

### **For Framework Maintainability**
- Clean separation between pattern definition and experiment execution
- Single source of truth for policy implementations
- Easier validation of configuration consistency

### **For User Experience**
- Architects define patterns once, reuse everywhere
- Experimenters select from predefined policies
- Analysts understand exactly what was tested

## **Migration Path**

### **Phase 1: Schema Update**
1. Add `parameter_bindings` to all policy definitions
2. Replace `component_policies` with `pattern_policy_references`
3. Add optional `experiment_design` section

### **Phase 2: Data Migration**
1. Convert existing JSON files to new format
2. Extract parameter values from CSV/analysis into pattern definitions
3. Update configuration mappings to use references

### **Phase 3: Framework Adaptation**
1. Update loader to resolve pattern policy references
2. Modify analysis to work with pattern-centric data
3. Update documentation and examples

## **Example Transformation**

**Before (Problematic):**
```json
// Pattern defines policy names but not values
"decisions": {
  "deployment_strategy": {
    "policies": {
      "one_device_low": { "description": "..." } // No bindings!
    }
  }
}

// Dataspace tries to map but doesn't define values
"component_policies": {
  "arch_example_pattern": "one_device_low" // What does this mean?
}
```

**After (Clear):**
```json
// Pattern defines complete policy
"decisions": {
  "deployment_strategy": {
    "policies": {
      "one_device_low": {
        "description": "...",
        "parameter_bindings": {  // Explicit values
          "levers": {"d1Services": 0, "d2Services": 0, "d3Services": 1}
        }
      }
    }
  }
}

// Dataspace simply references the policy
"pattern_policy_references": [
  {
    "component": "arch_example_pattern",
    "decision": "deployment_strategy",
    "policy": "one_device_low"
  }
]
```

## **Impact on ADEPT Framework Features**

### **Dual-Paradigm Analysis**
- **Enhanced**: Clearer mapping between policies and parameter values
- **Benefit**: More accurate scenario discovery and robustness analysis

### **Comparative Insights**
- **Improved**: Easier comparison of policies across different patterns
- **Benefit**: Better understanding of architectural trade-offs

### **Knowledge Curation**
- **Strengthened**: Patterns become curated architectural knowledge
- **Benefit**: Buildable catalog of validated architectural solutions

## **Conclusion**

The pattern-centric refactoring creates a more logical, maintainable, and powerful JSON schema for the ADEPT framework. It transforms patterns from incomplete templates to fully specified architectural solutions, enabling:

1. **True reusability** of architectural knowledge
2. **Clear traceability** from data to design decisions
3. **Flexible experimentation** with predefined policies
4. **Scalable pattern catalogs** that can grow independently of specific experiments

This approach aligns perfectly with ADEPT's goal of creating data-driven, explainable insights for software architecture decisions while maintaining the framework's flexibility for both static and adaptive system analysis.