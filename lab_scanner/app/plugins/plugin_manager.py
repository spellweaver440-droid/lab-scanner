"""
Plugin System - Dynamic Plugin Loader
Loads and executes plugins on demand
"""
import os
import sys
import importlib.util
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class PluginManager:
    """Manage plugin lifecycle and execution"""
    
    def __init__(self, plugin_dir: str = None):
        """
        Initialize plugin manager
        
        Args:
            plugin_dir: Directory containing plugins
        """
        self.plugin_dir = plugin_dir or os.path.join(
            os.path.dirname(__file__)
        )
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        """Dynamically load all plugins from plugin directory"""
        if not os.path.exists(self.plugin_dir):
            logger.warning(f"Plugin directory not found: {self.plugin_dir}")
            return
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                self._load_plugin(filename)

    def _load_plugin(self, filename: str):
        """Load a single plugin file"""
        try:
            module_name = filename[:-3]  # Remove .py
            filepath = os.path.join(self.plugin_dir, filename)
            
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                # Find plugin classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        hasattr(attr, 'run') and 
                        attr_name != 'BasePlugin'):
                        
                        self.plugins[attr_name] = attr
                        logger.info(f"Loaded plugin: {attr_name}")
        
        except Exception as e:
            logger.error(f"Error loading plugin {filename}: {str(e)}")

    def get_plugin(self, plugin_name: str):
        """Get plugin by name"""
        return self.plugins.get(plugin_name)

    def list_plugins(self) -> List[str]:
        """List all available plugins"""
        return list(self.plugins.keys())

    def run_plugin(self, plugin_name: str, target: str, port: int, service: str = "") -> Dict:
        """
        Execute a plugin
        
        Args:
            plugin_name: Name of plugin to run
            target: Target hostname/IP
            port: Target port
            service: Service name
            
        Returns:
            Dict: Plugin results
        """
        plugin_class = self.get_plugin(plugin_name)
        if not plugin_class:
            return {"error": f"Plugin not found: {plugin_name}"}
        
        try:
            plugin = plugin_class(target)
            result = plugin.run(target, port, service)
            return result
        except Exception as e:
            logger.error(f"Error running plugin {plugin_name}: {str(e)}")
            return {"error": str(e)}

    def run_all_plugins(self, target: str, port: int, service: str = "") -> List[Dict]:
        """
        Execute all available plugins
        
        Args:
            target: Target hostname/IP
            port: Target port
            service: Service name
            
        Returns:
            List[Dict]: Results from all plugins
        """
        results = []
        for plugin_name in self.list_plugins():
            result = self.run_plugin(plugin_name, target, port, service)
            results.append(result)
        
        return results
