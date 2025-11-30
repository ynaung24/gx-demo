"""
Great Expectations validation script for local CSV data.
Demonstrates both passing and failing validations using local sample data.
"""
import sys
import os
from pathlib import Path
from typing import Optional
import pandas as pd
import great_expectations as gx
import great_expectations.expectations as gxe


def create_expectation_suite(context, suite_name: str = "nba_player_stats_suite"):
    """
    Create an expectation suite with validation rules for NBA player stats.
    Uses local FileDataContext with ExpectationSuite API.
    
    Args:
        context: Great Expectations data context
        suite_name: Name of the expectation suite
    """
    # Delete existing suite if it exists
    try:
        context.suites.delete(suite_name)
    except:
        pass
    
    # Create ExpectationSuite using GX API (following gx-demo.py style)
    suite = gx.ExpectationSuite(name=suite_name)
    
    # Add expectations using gxe classes
    # Column existence expectations
    suite.add_expectation(gxe.ExpectColumnToExist(column="player_id"))
    suite.add_expectation(gxe.ExpectColumnToExist(column="player_name"))
    suite.add_expectation(gxe.ExpectColumnToExist(column="team"))
    suite.add_expectation(gxe.ExpectColumnToExist(column="points"))
    suite.add_expectation(gxe.ExpectColumnToExist(column="assists"))
    suite.add_expectation(gxe.ExpectColumnToExist(column="rebounds"))
    suite.add_expectation(gxe.ExpectColumnToExist(column="game_date"))
    suite.add_expectation(gxe.ExpectColumnToExist(column="minutes_played"))
    
    # Data type expectations
    suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="player_id", type_="int"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="player_name", type_="str"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="team", type_="str"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="points", type_="int"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="assists", type_="int"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="rebounds", type_="int"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="game_date", type_="str"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="minutes_played", type_="int"))
    
    # Not null expectations
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="player_id"))
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="player_name"))
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="team"))
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="points"))
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="assists"))
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="rebounds"))
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="game_date"))
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="minutes_played"))
    
    # Range expectations for numeric fields
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column="points", min_value=0, max_value=100))
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column="assists", min_value=0, max_value=30))
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column="rebounds", min_value=0, max_value=30))
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column="minutes_played", min_value=0, max_value=48))
    
    # Date format expectation
    suite.add_expectation(gxe.ExpectColumnValuesToMatchRegex(
        column="game_date",
        regex=r"^\d{4}-\d{2}-\d{2}$",
        mostly=1.0
    ))
    
    # Save suite to context
    context.suites.add(suite)
    
    print(f"✓ Created expectation suite: {suite_name} with {len(suite.expectations)} expectations")
    return suite_name


def validate_data(
    context,
    csv_path: str,
    suite_name: str = "nba_player_stats_suite"
):
    """
    Validate a local CSV file against the expectation suite.
    
    Args:
        context: Great Expectations data context
        csv_path: Path to CSV file (local)
        suite_name: Name of the expectation suite
    
    Returns:
        Validation result dictionary
    """
    print(f"\n{'='*60}")
    print(f"Validating: {csv_path}")
    print(f"{'='*60}")
    
    # Read CSV from local file
    try:
        df = pd.read_csv(csv_path)
        print(f"✓ Loaded CSV from local file: {len(df)} rows")
    except Exception as e:
        print(f"✗ Error reading CSV file: {e}")
        return None
    
    # Create batch using pandas_default (following gx-demo.py style)
    batch = context.data_sources.pandas_default.read_dataframe(df)
    
    # Get the expectation suite
    suite = context.suites.get(suite_name)
    
    # Validate using batch.validate(suite) - following gx-demo.py style
    validation_result = batch.validate(suite)
    success = validation_result.success
    
    print(f"✓ Validation completed")
    
    # Print summary
    print(f"\nValidation Result: {'✓ PASSED' if success else '✗ FAILED'}")
    print(f"Total Expectations: {len(validation_result.results)}")
    
    passed = sum(1 for r in validation_result.results if r.success)
    failed = len(validation_result.results) - passed
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    # Print failed expectations
    if not success:
        print(f"\n{'─'*60}")
        print("Failed Expectations:")
        print(f"{'─'*60}")
        for result in validation_result.results:
            if not result.success:
                # Get expectation type from the result
                if hasattr(result, 'expectation_config'):
                    expectation_type = getattr(result.expectation_config, 'expectation_type', None) or result.expectation_config.get("expectation_type", "N/A")
                    kwargs = getattr(result.expectation_config, 'kwargs', {}) or result.expectation_config.get("kwargs", {})
                else:
                    expectation_type = "N/A"
                    kwargs = {}
                column = kwargs.get('column', 'N/A')
                print(f"\n✗ {expectation_type}")
                print(f"  Column: {column}")
                if hasattr(result, 'result') and result.result:
                    if 'unexpected_count' in result.result:
                        print(f"  Unexpected values: {result.result['unexpected_count']}")
                    if 'unexpected_percent' in result.result:
                        print(f"  Unexpected percent: {result.result['unexpected_percent']:.2f}%")
                    if 'unexpected_list' in result.result and len(result.result['unexpected_list']) > 0:
                        unexpected = result.result['unexpected_list'][:5]  # Show first 5
                        print(f"  Sample unexpected values: {unexpected}")
    
    return validation_result


def main():
    """Main function to run validations on local sample data."""
    # Get script directory and sample data path
    script_dir = Path(__file__).parent
    sample_data_dir = script_dir / "sample_data"
    
    # Initialize local GX context
    # Use a fresh context directory to avoid GCS config dependencies
    print("Initializing Great Expectations (local mode)...")
    try:
        # Create a new context in a local directory
        gx_root = script_dir / "gx_local"
        context = gx.get_context(context_root_dir=str(gx_root))
        print("✓ GX context initialized (local mode)")
    except Exception as e:
        print(f"✗ Error initializing GX context: {e}")
        sys.exit(1)
    
    # Create expectation suite
    suite_name = create_expectation_suite(context)
    
    # Validate good data
    print("\n" + "="*60)
    print("DEMO 1: Validating GOOD Data")
    print("="*60)
    good_data_path = sample_data_dir / "good_data.csv"
    good_result = validate_data(
        context,
        csv_path=str(good_data_path),
        suite_name=suite_name
    )
    
    # Validate bad data
    print("\n" + "="*60)
    print("DEMO 2: Validating BAD Data")
    print("="*60)
    bad_data_path = sample_data_dir / "bad_data.csv"
    bad_result = validate_data(
        context,
        csv_path=str(bad_data_path),
        suite_name=suite_name
    )
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    if good_result:
        print(f"Good Data: {'✓ PASSED' if good_result.success else '✗ FAILED'}")
    if bad_result:
        print(f"Bad Data: {'✓ PASSED' if bad_result.success else '✗ FAILED'}")
    
    # Build data docs for local viewing
    print("\n" + "="*60)
    print("Building Data Docs...")
    print("="*60)
    try:
        context.build_data_docs()
        print("✓ Data Docs built successfully")
        
        # Get data docs URLs
        try:
            docs_urls = context.get_docs_sites_urls()
            if docs_urls and isinstance(docs_urls, dict):
                print("\nData Docs URLs:")
                for site_name, url in docs_urls.items():
                    print(f"  {site_name}: {url}")
            else:
                docs_path = script_dir / "gx_local" / "data_docs" / "index.html"
                print(f"\nLocal Data Docs: {docs_path}")
                print(f"  Open this file in your browser to view validation results")
        except:
            docs_path = script_dir / "gx_local" / "data_docs" / "index.html"
            print(f"\nLocal Data Docs: {docs_path}")
            print(f"  Open this file in your browser to view validation results")
    except Exception as e:
        print(f"⚠️  Warning: Could not build data docs: {e}")
        docs_path = script_dir / "gx_local" / "data_docs" / "index.html"
        print(f"Local Data Docs should be at: {docs_path}")


if __name__ == "__main__":
    main()

