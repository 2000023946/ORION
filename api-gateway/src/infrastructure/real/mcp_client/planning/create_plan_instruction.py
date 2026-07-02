CREATE_PLAN_INSTRUCTION = """
========================
OUTPUT FORMAT
========================

Return ONLY valid JSON.

Example:
{
  "edges": [
    ["START", "VECTOR_SEARCH_TOOL"],
    ["VECTOR_SEARCH_TOOL", "METADATA_FILTER_TOOL"],
    ["METADATA_FILTER_TOOL", "END"]
  ]
}

========================
STRICT RULES (NON-NEGOTIABLE)
========================

1. Output MUST be valid JSON with exactly:
   {
     "edges": [...]
   }

2. Each edge MUST be:
   ["SOURCE_NODE", "DESTINATION_NODE"]

3. You are ONLY allowed to create an edge if BOTH are true:

   (A) DATA FLOW RULE (HARD REQUIREMENT)
   - The SOURCE produces an output field
   - The DESTINATION requires that SAME field as input
   - Field name AND type must match exactly

   (B) FEASIBILITY RULE
   - The destination input must be fully satisfied by the source output

4. DO NOT infer semantic relationships.
   - "documents can be used as query" is INVALID
   - "IDs imply documents" is INVALID
   - Only explicit IO matching is allowed

5. START RULE:
   - START provides ONLY:
     query: str

   So only tools that take `query` may connect to START.

6. END RULE:
   - Every valid execution path MUST end in END
   - A node connects to END ONLY IF:
     it produces final output not consumed by any other tool

7. FULL PATH RULE (VERY IMPORTANT):
   - Every tool included MUST lie on at least one path:
     START → ... → END

8. NO ORPHANS:
   - If a tool cannot be fully connected via IO rules, DO NOT include it

9. NO FORCED CHAINS:
   - Do NOT chain tools just because they are in a pipeline
   - Example (WRONG):
     VECTOR_SEARCH → METADATA_FILTER → DB_FILTER
   - unless DB_FILTER input explicitly matches METADATA output

10. MULTIPLE PATHS ALLOWED:
   - You may branch only if IO supports it

========================
OUTPUT CONSTRAINTS
========================

- NO markdown
- NO explanation
- NO extra text
- NO comments
- ONLY JSON
"""