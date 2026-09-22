# milk_data_find

Finding missing data from missing ID tags.

## Project objective

The goal of this project is to identify records with missing cow ID tags and assign the most likely cow IDs using the other available data, while keeping the process understandable, reproducible, and easy to validate.

## Proposed timeline

This is an initial working timeline and can be refined during our Wednesday discussion.

| Phase | Activities | Expected output | Target timing |
|---|---|---|---|
| 1. Understand the data | Inventory files, inspect columns and data types, identify missing IDs, review duplicate records, and understand how the data was collected. | Data dictionary and initial data-quality report | Before Wednesday |
| 2. Standardize the data | Fix column names, units, date/time formats, categorical values, and naming conventions. Preserve the original values separately. | Clean, consistently formatted analysis dataset | Week 1 |
| 3. Establish data lineage | Record the source file, transformation, version, and row-level or batch-level changes made during cleaning. | Reproducible transformation notes and lineage log | Week 1 |
| 4. Explore patterns | Calculate descriptive statistics and visualize milk yield and the other available factors by known cow ID, date, and relevant grouping variables. | Exploratory analysis and plausible value ranges for each cow | Week 2 |
| 5. Build candidate matching approaches | Start with a rules- and distance-based baseline, then evaluate statistical or machine-learning approaches if they add value. | Baseline matcher and candidate cow IDs with confidence scores | Week 2–3 |
| 6. Test and validate | Hide IDs from known records, run the matching process, compare predictions with the true IDs, and inspect ambiguous and incorrect matches. | Validation metrics, error analysis, and review samples | Week 3 |
| 7. Refine and document | Tune thresholds, resolve data-quality issues, document limitations, and produce the final output with an audit trail. | Final matched dataset, documentation, and recommendations | Week 4 |

## Working environment

The initial plan is to work **locally** so that the raw farm data remains under our control and the analysis can be run quickly while the approach is being developed. The primary IDE will be **Visual Studio Code**, using a Python environment and notebooks for exploration. Scripts will be used for repeatable cleaning and matching steps.

If the dataset becomes too large for the local machine, or if collaboration and scheduled runs become important, the project can be moved to a cloud environment such as **GitHub Codespaces** or a managed notebook platform. The code and environment configuration should be kept portable so that moving to the cloud does not change the analysis.

## Strategy brainstorm

### 1. Understand the available evidence

Before selecting a model, I will determine which fields are reliable and which are likely to identify a cow. Possible factors include:

- Milk yield
- Date and time of collection
- Lactation or production stage
- Age or parity
- Breed or group
- Feed, health, or management information
- Any location, equipment, or sequence information

I will also check whether the same cow appears multiple times and whether measurements are recorded at a regular frequency. This will help prevent us from treating repeated observations as independent evidence when they are not.

### 2. Create a reproducible data-cleaning process

The raw data will remain unchanged. Cleaning will be performed through documented scripts or notebooks that:

- Standardize column names and naming conventions
- Convert units and data types consistently
- Parse dates and times
- Handle missing, impossible, or outlier values
- Preserve the original row identifier
- Add a record describing each transformation

Every output should be traceable back to its source file and original row wherever possible.

### 3. Begin with an interpretable baseline

The first matching method should be simple and explainable rather than immediately using a complex model. For each record with a missing ID, I will compare its available measurements with records that have known IDs and generate a ranked list of candidate cows.

Possible baseline methods include:

- Rule-based filtering using date, herd/group, and plausible ranges
- Standardized distance or nearest-neighbor matching across the available factors
- Weighted distances, giving greater weight to variables that are more stable or discriminative
- Comparison with a cow's historical profile rather than only one individual record

The baseline should produce both a proposed ID and a confidence score or margin between the first- and second-best candidates.

### 4. Consider model choices

After establishing the baseline, we can discuss whether a more formal model is justified. Options to evaluate include:

- **Nearest neighbors:** interpretable and useful when similar records should belong to the same cow.
- **Random forest or gradient-boosted trees:** useful for nonlinear relationships and interactions among variables, with feature-importance analysis for interpretation.
- **Probabilistic matching:** estimates the likelihood that a record belongs to each cow and naturally represents uncertainty.
- **Clustering:** useful for exploring whether records form stable cow-level groups, but not necessarily sufficient by itself to assign real IDs.
- **Sequence or time-series methods:** worth considering if the order of observations and changes over time provide important identifying information.

The preferred model should be selected based on validation performance, interpretability, data volume, and the cost of an incorrect assignment. A model should not be used simply because it is more complex.

### 5. Test without relying on the missing-ID records

Because the true answer is unknown for the missing records, testing will use records whose IDs are known:

1. Select known records and temporarily hide their IDs.
2. Run the complete cleaning and matching workflow.
3. Compare predicted IDs with the known IDs.
4. Repeat this using multiple splits or time-based holdouts.
5. Review errors, especially cases where the model was highly confident but wrong.

Potential measures include top-1 accuracy, top-3 candidate coverage, precision at the selected confidence threshold, confusion between similar cows, and the percentage of records left unresolved. A time-based split may be particularly important if future records are meant to be matched using historical data.

### 6. Manage uncertainty and manual review

Not every record should be forced into a cow ID. Records with weak evidence, conflicting fields, or nearly tied candidate scores should be marked for manual review or left unresolved. The output should distinguish among:

- High-confidence automatic matches
- Lower-confidence suggested matches
- Records requiring manual review
- Records for which no plausible match was found

This is safer than presenting every prediction as certain.

### 7. Track data lineage and reproducibility

For each delivered dataset, I plan to record:

- Source file name, date, and version or checksum
- Original row identifier
- Cleaning and transformation steps
- Features used for matching
- Model or matching method and version
- Parameters, weights, and thresholds
- Candidate IDs and confidence scores
- Final decision and whether it was manually reviewed
- Code version or Git commit used to create the output

This will let us explain why a particular ID was assigned and rerun the process when new data arrives.

## Initial success criteria

The project will be considered successful when it produces a documented and repeatable workflow that:

1. Standardizes the source data without losing the raw records.
2. Assigns likely IDs only when the evidence is sufficient.
3. Provides confidence scores and an audit trail for every proposed match.
4. Demonstrates its performance on known records that were hidden during testing.
5. Clearly identifies uncertain cases for manual review.

If the results are reliable, then we can shout hooray!
