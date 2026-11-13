"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    import sys
    sku = data['sku']
    if sku not in data['stock']:
        raise ValueError('Unknown SKU')
    options = {'tools': ['mcp__inventory__get_stock'], 'allowed_tools': ['mcp__inventory__get_stock'],
               'mcp_servers': {'inventory': {'command': sys.executable, 'args': [str(agent.root / 'server.py')]}}}
    answer = await agent.ask('inventory', 'Call the inventory get_stock tool for the SKU. Distinguish zero stock from an unknown SKU.',
                            {'sku': sku}, f"{sku} has {data['stock'][sku]} units.", sdk=options)
    return {'sku': sku, 'reference_stock': data['stock'][sku], 'answer': answer, 'transport': 'stdio'}
