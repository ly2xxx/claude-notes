#!/usr/bin/env python3
"""
API Client - Reads endpoint definitions from knowledge/api-endpoints.yaml

This demonstrates WHY YAML is better than Markdown for knowledge files:
- Simple parsing (2 lines!)
- Type-safe (requires_auth is boolean, not string)
- Easy querying (dictionary access, not regex)
- Maintainable (update YAML without changing this code)
"""

import yaml
import os
from pathlib import Path


class APIClient:
    """
    API Client that reads endpoint configurations from YAML knowledge base.
    
    Notice how SIMPLE this is because we use YAML:
    - Load YAML file: 2 lines of code
    - Access endpoint: simple dictionary lookup
    - Type-safe: boolean values stay boolean
    """
    
    def __init__(self, knowledge_dir=None):
        """Initialize client and load endpoints from YAML."""
        if knowledge_dir is None:
            # Default to knowledge/ folder relative to this script
            script_dir = Path(__file__).parent
            knowledge_dir = script_dir.parent / "knowledge"
        
        self.knowledge_dir = Path(knowledge_dir)
        self.endpoints = self._load_endpoints()
    
    def _load_endpoints(self):
        """
        Load API endpoints from YAML file.
        
        THIS IS THE KEY BENEFIT OF YAML:
        Just 2 lines to load structured data!
        
        If this was Markdown, we'd need:
        - Complex regex patterns
        - Fragile string parsing
        - Type conversion (everything is string)
        - Error-prone manual parsing
        """
        endpoints_file = self.knowledge_dir / "api-endpoints.yaml"
        
        with open(endpoints_file, 'r') as f:
            data = yaml.safe_load(f)  # ← THAT'S IT! Clean and simple.
        
        return data
    
    def get_endpoint(self, service, action):
        """
        Get endpoint details for a service and action.
        
        YAML Benefits shown here:
        - Dictionary access (not regex parsing!)
        - Structured data (guaranteed format)
        - Type-safe (method is string, requires_auth is boolean)
        
        Args:
            service: Service name (e.g., 'user_service')
            action: Action name (e.g., 'get_user')
        
        Returns:
            dict: Endpoint configuration
        
        Raises:
            ValueError: If service or action not found
        """
        if service not in self.endpoints:
            available = list(self.endpoints.keys())
            raise ValueError(f"Service '{service}' not found. Available: {available}")
        
        service_data = self.endpoints[service]
        
        if action not in service_data['endpoints']:
            available = list(service_data['endpoints'].keys())
            raise ValueError(f"Action '{action}' not found in '{service}'. Available: {available}")
        
        endpoint = service_data['endpoints'][action]
        
        # Combine base URL and path
        base_url = service_data['base_url']
        path = endpoint['path']
        
        return {
            'url': f"{base_url}{path}",
            'method': endpoint['method'],
            'description': endpoint['description'],
            'requires_auth': endpoint['requires_auth'],
            'path_template': path
        }
    
    def list_services(self):
        """List all available services."""
        return list(self.endpoints.keys())
    
    def list_actions(self, service):
        """List all actions for a service."""
        if service not in self.endpoints:
            raise ValueError(f"Service '{service}' not found")
        
        return list(self.endpoints[service]['endpoints'].keys())
    
    def call(self, service, action, **kwargs):
        """
        Make an API call (simulated for this demo).
        
        In a real implementation, this would:
        1. Get endpoint config from YAML
        2. Format the URL with kwargs
        3. Make the HTTP request
        4. Return the response
        
        Args:
            service: Service name
            action: Action name
            **kwargs: URL parameters or request body
        
        Returns:
            dict: Simulated response
        """
        endpoint = self.get_endpoint(service, action)
        
        # Simulate formatting URL with parameters
        url = endpoint['url']
        for key, value in kwargs.items():
            url = url.replace(f"{{{key}}}", str(value))
        
        # Simulated response
        return {
            'status': 'success',
            'endpoint': endpoint,
            'formatted_url': url,
            'parameters': kwargs,
            'message': f"Would call: {endpoint['method']} {url}"
        }


# ============================================
# Demo Usage
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("API Client Demo - YAML Knowledge Benefits")
    print("=" * 60)
    print()
    
    # Initialize client (loads YAML automatically)
    client = APIClient()
    
    print("📦 Available Services:")
    for service in client.list_services():
        print(f"  - {service}")
    print()
    
    print("🔧 User Service Actions:")
    for action in client.list_actions('user_service'):
        print(f"  - {action}")
    print()
    
    print("=" * 60)
    print("Example 1: Get User Endpoint")
    print("=" * 60)
    endpoint = client.get_endpoint('user_service', 'get_user')
    print(f"Method: {endpoint['method']}")
    print(f"URL: {endpoint['url']}")
    print(f"Description: {endpoint['description']}")
    print(f"Requires Auth: {endpoint['requires_auth']}")  # ← Notice: boolean, not string!
    print()
    
    print("=" * 60)
    print("Example 2: Simulated API Call")
    print("=" * 60)
    response = client.call('user_service', 'get_user', user_id=123)
    print(f"Status: {response['status']}")
    print(f"Method: {response['endpoint']['method']}")
    print(f"URL: {response['formatted_url']}")
    print()
    
    print("=" * 60)
    print("Why YAML Wins")
    print("=" * 60)
    print("✅ Loaded endpoints with just: yaml.safe_load(file)")
    print("✅ Accessed data with: data['user_service']['endpoints']['get_user']")
    print("✅ Type-safe: requires_auth is boolean, not string")
    print("✅ Easy to query: list_services(), list_actions()")
    print("✅ Maintainable: update YAML without changing this code!")
    print()
    print("❌ If this was Markdown:")
    print("   - Complex regex parsing required")
    print("   - Fragile (format changes break code)")
    print("   - Everything would be strings")
    print("   - Hard to query programmatically")
    print()
    
    print("🎯 RESULT: YAML makes scripts simple, reliable, and maintainable!")
