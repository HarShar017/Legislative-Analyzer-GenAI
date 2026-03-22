from pipeline import process_document

SAMPLE_TEXT = """
BILL: Comprehensive Healthcare Reform Act of 2024

SECTION 1: EXPANSION OF COVERAGE
The government shall establish a mandatory healthcare coverage system for all 
residents earning below the median household income. This amendment modifies 
existing healthcare statutes to ensure coverage begins by January 1, 2025.
Affected citizens include low-income families, seniors, and individuals with
pre-existing conditions. The state healthcare department shall manage enrollment.

SECTION 2: FINANCIAL IMPLICATIONS
Annual program cost: $2.5 billion
Federal matching funds: 60%
State contribution: 40%
Implementation costs: $150 million
Ongoing operational budget: $2.35 billion annually
Penalties for non-compliance: $5,000 per violation
Provider compensation rate: 90% of Medicare rates

SECTION 3: AFFECTED PARTIES
This act shall apply to:
- Individual citizens earning below $75,000 annually
- Small businesses with fewer than 50 employees
- State health departments and agencies
- Federal healthcare agencies (CMS, HHS)
- Insurance providers and hospitals statewide
- Healthcare workers and medical professionals
- Pharmaceutical companies operating in state

SECTION 4: IMPLEMENTATION TIMELINE
- Effective Date: January 1, 2025
- Implementation Phase 1: January 2025 - June 2025 (setup and enrollment)
- Implementation Phase 2: July 1, 2025 (coverage begins)
- Full rollout: December 31, 2025
- Annual review date: September 1 each year

SECTION 5: REGULATORY REQUIREMENTS
Healthcare providers must:
- Achieve compliance by effective date
- Maintain detailed records of claims and enrollments
- Report monthly statistics to state agency
- Implement new billing systems
- Train staff on new procedures
- Ensure data security per HIPAA requirements

Violations shall result in civil penalties up to $10,000 per incident.
The Department of Health and Human Services shall enforce compliance.

SECTION 6: RISKS AND CONCERNS
Risk factors include:
- Potential disruption to existing provider networks during transition
- Administrative burden on small healthcare facilities with limited IT resources
- Possible insurance premium increases for existing coverage
- Data privacy concerns with expanded coverage information collection
- Provider payment delays during system implementation
- Potential workforce shortages in rural healthcare facilities
- Risk of provider network reductions in underserved areas

SECTION 7: DISPUTE RESOLUTION
Any disputes arising from this act shall be resolved through:
1. Administrative appeal within 30 days
2. State healthcare commission review
3. Federal arbitration if necessary
The state shall maintain an ombudsman office for citizen complaints.
"""

def main():
    print("\n" + "="*60)
    print("TESTING AI LEGISLATIVE ANALYZER PIPELINE")
    print("="*60)
    print(f"\nProcessing sample text ({len(SAMPLE_TEXT)} characters)...")
    print("\nSample content:")
    print("-" * 60)
    print(SAMPLE_TEXT[:300] + "...\n")
    print("-" * 60)
    result = process_document(SAMPLE_TEXT)
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"\nStatus: {result['status']}")
    print(f"Chunks processed: {result['num_chunks']}")
    stats = result['chunk_stats']
    print(f"\nCompression Statistics:")
    print(f"  - Original tokens: {stats['original_total_tokens']}")
    print(f"  - Compressed tokens: {stats['compressed_total_tokens']}")
    compression_pct = (1 - stats['compressed_total_tokens'] / stats['original_total_tokens']) * 100
    print(f"  - Compression rate: {compression_pct:.1f}%")
    print(f"\n" + "="*60)
    print("ANALYSIS OUTPUT")
    print("="*60)
    print(result['summary'])
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
