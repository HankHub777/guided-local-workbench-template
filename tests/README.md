# Tests

Start with small checks that protect the business workflow:

1. Fixture spreadsheet/JSON validates against the shared schema.
2. ETL produces expected JSON for representative input.
3. A critical UI calculation or filter produces the known result.

Add end-to-end tests only once the tool is shared, deployed, or business-critical.
