# Great Expectations Data Validation Demo

This demo showcases how Great Expectations (GX) would work if integrated into our project. It demonstrates data validation using local CSV files to test validation functions, showing both **passing** and **failing** validation scenarios.

## Overview

This is a proof-of-concept demonstrating how Great Expectations could be integrated into our data pipeline. The demo validates NBA player statistics data from local CSV files against a set of data quality expectations. It includes:

- **Good Data**: A CSV file with valid, properly formatted data that passes all validations
- **Bad Data**: A CSV file with various data quality issues (invalid types, missing values, out-of-range values, etc.) that fails validations

## What Gets Validated

The expectation suite validates:

1. **Column Existence**: All required columns are present
2. **Data Types**: Columns have the correct data types (int, str)
3. **Not Null**: Required fields are not null/empty
4. **Value Ranges**: Numeric fields are within reasonable ranges:
   - Points: 0-100
   - Assists: 0-30
   - Rebounds: 0-30
   - Minutes Played: 0-48
5. **Date Format**: Game dates match YYYY-MM-DD format

## Setup

### 1. Install Dependencies

```bash
cd gx-demo
pip install -r requirements.txt
```

### 2. Sample Data

The demo uses local CSV files from the `sample_data/` directory:
- `sample_data/good_data.csv` - Valid data that passes all validations
- `sample_data/bad_data.csv` - Invalid data that fails various validations

No additional configuration is needed - the script reads directly from these local files.

## Running the Demo

### Run Validations

```bash
python validate_gcs_data.py
```

This script will:

1. Initialize Great Expectations context (local mode)
2. Create an expectation suite with validation rules
3. Validate the **good data** CSV from `sample_data/good_data.csv`
4. Validate the **bad data** CSV from `sample_data/bad_data.csv`
5. Display validation results showing which expectations passed/failed
6. Generate HTML data docs for viewing detailed validation results

### Expected Output

**Good Data Validation:**
```
✓ PASSED
Total Expectations: 20+
Passed: 20+
Failed: 0
```

**Bad Data Validation:**
```
✗ FAILED
Total Expectations: 20+
Passed: 15
Failed: 5+

Failed Expectations:
✗ expect_column_values_to_be_of_type
  Column: points
  Unexpected values: 2

✗ expect_column_values_to_be_between
  Column: minutes_played
  Unexpected values: 1
  ...
```

## Sample Data Details

### Good Data (`good_data.csv`)

Contains 10 rows of valid NBA player statistics:
- All fields properly typed
- All values within expected ranges
- No missing values
- Proper date formatting

### Bad Data (`bad_data.csv`)

Contains 10 rows with various data quality issues:
- **Row 2**: Invalid points value ("invalid" instead of integer)
- **Row 3**: Invalid date format ("invalid-date" instead of YYYY-MM-DD)
- **Row 4**: Minutes played out of range (999, max is 48)
- **Row 6**: Missing player name (empty string)
- **Row 7**: Negative minutes played (-5)
- **Row 8**: Points as string ("abc" instead of integer)

## Viewing Data Docs

After running validations, Great Expectations generates HTML data docs. Open:

```
gx_local/uncommitted/data_docs/local_site/index.html
```

This provides a detailed, interactive view of:
- All expectations defined
- Validation results for each batch
- Statistics and visualizations
- Failed expectations with details

## Great Expectations UI (No-Code Interface)

Great Expectations includes a web-based UI that provides a **no-code interface** for creating and managing data quality expectations. This UI demonstrates how non-technical users could interact with Great Expectations if it were connected to our production databases.

### Key Features

The GX UI allows users to:

- **Browse Data Sources**: Connect to and explore data from various sources including:
  - Google Cloud Storage (GCS)
  - Amazon S3
  - Snowflake
  - Other SQL databases
  - Local files

- **Create Expectations Visually**: Build data quality expectations through an intuitive interface without writing code:
  - Select columns to validate
  - Choose expectation types from a dropdown
  - Configure parameters through forms
  - Preview results before saving

- **Review Validation Results**: View validation results in an interactive dashboard with:
  - Pass/fail indicators
  - Detailed statistics
  - Visualizations
  - Drill-down capabilities

- **Manage Expectation Suites**: Organize and manage multiple expectation suites for different data sources or use cases

### Screenshots

See the `screenshots/` directory for examples of the GX UI in action, demonstrating:
- The expectation creation interface
- Validation result dashboards
- Data source connection options

### Integration Potential

If we connect Great Expectations to our production data sources (GCS, S3, Snowflake, etc.), the UI would enable:
- **Business users** to define and modify data quality rules without coding
- **Data analysts** to quickly create validation checks through the interface
- **Data engineers** to review and approve expectations created by other team members
- **Stakeholders** to monitor data quality through accessible dashboards

This no-code approach makes data quality management more accessible across the organization while maintaining the power and flexibility of programmatic validation when needed.

## Customization

### Adding More Expectations

Edit `validate_gcs_data.py` and add more expectations in the `create_expectation_suite()` function:

```python
# Example: Add uniqueness check
validator.expect_column_values_to_be_unique("player_id")

# Example: Add value set check
validator.expect_column_values_to_be_in_set("team", ["Lakers", "Warriors", "Suns", ...])
```

### Validating Different Data

To validate different CSV files:

1. Place your CSV file in the `sample_data/` directory (or update the path in the script)
2. Modify the `csv_path` parameter in `validate_data()` calls in `validate_gcs_data.py`
3. Update the expectation suite in `create_expectation_suite()` if your schema differs

## Integration with Existing Pipeline

This demo serves as a proof-of-concept for how Great Expectations could be integrated into our existing data pipeline:

1. **After Data Processing**: Run validations after data is processed/written
2. **Scheduled Validations**: Integrate validation checks into scheduled data pipeline runs
3. **Alerting**: Configure GX to send alerts when validations fail
4. **Data Quality Dashboard**: Use GX Data Docs as a data quality dashboard
5. **Testing Functions**: Use `validate_gcs_data.py` to test validation functions with sample data before integration
6. **No-Code UI**: Once connected to production databases (GCS, S3, Snowflake), enable business users to create and manage expectations through the GX web UI without coding

## Troubleshooting

### Import Errors

If you see import errors:
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python environment

### File Not Found Errors

If CSV files aren't found:
- Verify the `sample_data/` directory exists in the project root
- Check that `good_data.csv` and `bad_data.csv` are present in `sample_data/`
- Ensure the script is being run from the project root directory
