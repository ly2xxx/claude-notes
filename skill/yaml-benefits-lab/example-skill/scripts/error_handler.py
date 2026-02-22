#!/usr/bin/env python3
"""
Error Handler - Reads error codes from knowledge/error-codes.yaml

This demonstrates WHY YAML is better than Markdown for knowledge files:
- Clean parsing (no regex!)
- Type-safe (severity levels)
- Easy filtering (by category, severity)
- Queryable (dictionary operations)
"""

import yaml
from pathlib import Path
from collections import defaultdict


class ErrorHandler:
    """
    Error handler that reads error code definitions from YAML knowledge base.
    
    Notice the simplicity:
    - Load errors: 2 lines
    - Query errors: dictionary lookup
    - Filter errors: simple list comprehension
    """
    
    def __init__(self, knowledge_dir=None):
        """Initialize handler and load error codes from YAML."""
        if knowledge_dir is None:
            script_dir = Path(__file__).parent
            knowledge_dir = script_dir.parent / "knowledge"
        
        self.knowledge_dir = Path(knowledge_dir)
        self.error_codes = self._load_error_codes()
    
    def _load_error_codes(self):
        """
        Load error codes from YAML file.
        
        YAML BENEFIT: Simple, clean loading!
        
        If this was Markdown:
        - Need regex to parse "1002: User not found"
        - Manual string splitting for fields
        - No type safety (severity could be typo'd)
        - Fragile if format changes
        """
        error_file = self.knowledge_dir / "error-codes.yaml"
        
        with open(error_file, 'r') as f:
            data = yaml.safe_load(f)
        
        return data['error_codes']
    
    def get_error_info(self, code):
        """
        Get error information by code.
        
        YAML BENEFIT: Simple dictionary lookup!
        
        Args:
            code: Error code (int or string)
        
        Returns:
            dict: Error details
        
        Raises:
            KeyError: If error code not found
        """
        code = int(code)  # Ensure integer key
        
        if code not in self.error_codes:
            raise KeyError(f"Error code {code} not found in knowledge base")
        
        return self.error_codes[code]
    
    def get_errors_by_severity(self, severity):
        """
        Get all errors of a specific severity level.
        
        YAML BENEFIT: Easy filtering with list comprehension!
        
        Args:
            severity: One of 'critical', 'error', 'warning', 'info'
        
        Returns:
            dict: Error codes and their details
        """
        return {
            code: info
            for code, info in self.error_codes.items()
            if info['severity'] == severity
        }
    
    def get_errors_by_category(self, category):
        """
        Get all errors in a specific category.
        
        YAML BENEFIT: Structured data makes filtering trivial!
        
        Args:
            category: Category name (e.g., 'validation', 'payment', 'auth')
        
        Returns:
            dict: Error codes and their details
        """
        return {
            code: info
            for code, info in self.error_codes.items()
            if info['category'] == category
        }
    
    def get_categories(self):
        """Get all unique error categories."""
        return sorted(set(
            info['category']
            for info in self.error_codes.values()
        ))
    
    def get_severity_levels(self):
        """Get all unique severity levels."""
        return sorted(set(
            info['severity']
            for info in self.error_codes.values()
        ), key=lambda x: ['info', 'warning', 'error', 'critical'].index(x))
    
    def format_error_message(self, code, include_action=True):
        """
        Format a user-friendly error message.
        
        YAML BENEFIT: Structured data makes formatting easy!
        
        Args:
            code: Error code
            include_action: Whether to include action guidance
        
        Returns:
            str: Formatted error message
        """
        error = self.get_error_info(code)
        
        severity_emoji = {
            'critical': '🔴',
            'error': '⚠️',
            'warning': '⚡',
            'info': 'ℹ️'
        }
        
        emoji = severity_emoji.get(error['severity'], '❓')
        
        msg = f"{emoji} Error {code} ({error['severity'].upper()}): {error['message']}"
        
        if include_action:
            msg += f"\n   → Action: {error['action']}"
        
        return msg
    
    def get_error_stats(self):
        """
        Get statistics about error codes.
        
        YAML BENEFIT: Easy data analysis!
        
        Returns:
            dict: Statistics
        """
        stats = {
            'total_errors': len(self.error_codes),
            'by_severity': defaultdict(int),
            'by_category': defaultdict(int)
        }
        
        for info in self.error_codes.values():
            stats['by_severity'][info['severity']] += 1
            stats['by_category'][info['category']] += 1
        
        return dict(stats)


# ============================================
# Demo Usage
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("Error Handler Demo - YAML Knowledge Benefits")
    print("=" * 60)
    print()
    
    # Initialize handler (loads YAML automatically)
    handler = ErrorHandler()
    
    print("=" * 60)
    print("Example 1: Get Specific Error")
    print("=" * 60)
    error = handler.get_error_info(1002)
    print(f"Code: 1002")
    print(f"Message: {error['message']}")
    print(f"Severity: {error['severity']}")
    print(f"Category: {error['category']}")
    print(f"Action: {error['action']}")
    print()
    
    print("=" * 60)
    print("Example 2: Formatted Error Message")
    print("=" * 60)
    print(handler.format_error_message(1002))
    print()
    print(handler.format_error_message(2001))
    print()
    print(handler.format_error_message(9004))
    print()
    
    print("=" * 60)
    print("Example 3: Filter by Severity")
    print("=" * 60)
    critical_errors = handler.get_errors_by_severity('critical')
    print(f"Critical Errors ({len(critical_errors)}):")
    for code, info in critical_errors.items():
        print(f"  {code}: {info['message']}")
    print()
    
    print("=" * 60)
    print("Example 4: Filter by Category")
    print("=" * 60)
    validation_errors = handler.get_errors_by_category('validation')
    print(f"Validation Errors ({len(validation_errors)}):")
    for code, info in validation_errors.items():
        print(f"  {code}: {info['message']}")
    print()
    
    print("=" * 60)
    print("Example 5: Statistics")
    print("=" * 60)
    stats = handler.get_error_stats()
    print(f"Total Errors: {stats['total_errors']}")
    print()
    print("By Severity:")
    for severity, count in sorted(stats['by_severity'].items()):
        print(f"  {severity}: {count}")
    print()
    print("By Category:")
    for category, count in sorted(stats['by_category'].items()):
        print(f"  {category}: {count}")
    print()
    
    print("=" * 60)
    print("Why YAML Wins")
    print("=" * 60)
    print("✅ Loaded errors with just: yaml.safe_load(file)")
    print("✅ Queried errors: handler.get_error_info(1002)")
    print("✅ Filtered easily: get_errors_by_severity('critical')")
    print("✅ Type-safe: severity levels are strings, not free-form")
    print("✅ Analyzable: get_error_stats() works because structure is guaranteed")
    print()
    print("❌ If this was Markdown:")
    print("   - Parsing '- 1002: User not found' requires regex")
    print("   - Filtering by severity would be error-prone")
    print("   - Statistics would require manual counting")
    print("   - No guarantee of consistent structure")
    print()
    
    print("🎯 RESULT: YAML makes error handling simple and powerful!")
